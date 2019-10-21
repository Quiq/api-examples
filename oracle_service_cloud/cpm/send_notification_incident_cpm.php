<?php

/*
 * CPMObjectEventHandler: sendNotificationIncident
 * Package: RN
 * Objects: Incident
 * Actions: Create, Update
 * Version: 1.2
 */

use \RightNow\CPM\v1 as RNCPM;
use \RightNow\Connect\v1_2 as RNCPHP;

//----------------------------------------------------------------------------
// Description: Sends a notification out via Quiq
//----------------------------------------------------------------------------
class sendNotificationIncident implements RNCPM\ObjectEventHandler {

    public static function apply($run_mode, $action, $inc, $n_cycles) {
        $contactId = $inc->PrimaryContact->ID;
        $contact = RNCPHP\Contact::fetch($contactId);
 
        foreach ($contact->Phones as $phoneStruct) {
            $key = ''; //TODO - replace with your own values
            $secret = ''; //TODO - replace with your own values
            $tenantBaseUrl = ''; // TODO - replace with your own values    
   
            $contactPhoneNumber = $phoneStruct->Number;
            $contactPoint = '';
            $topic = '';
            $messageText = 'Hello '.$contact->Name->First.' '.$contact->Name->Last.' this is an example outbound notification'; //TODO - replace with your own values
    
            $precedence = array(array("platform" => "SMS"));
            $messageMap = array("default" => array("text" => $messageText));
    
            $searchInfo = array("phoneNumber" => $contactPhoneNumber);
            $notification = array("searchInfo" => $searchInfo, "integrations" => array(), "precedence" => $precedence, "messageMap" => $messageMap);
            $notifications = array($notification);
    
            $payload= json_encode(array("contactPoint" => $contactPoint, "notifications" => $notifications, "topic" => $topic));
    
            load_curl();
            $url = $tenantBaseUrl . "/api/v1/messaging/notify";
    
            $ch = curl_init($url);
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            curl_setopt($ch, CURLOPT_USERPWD, $key . ":" . $secret);
            curl_setopt($ch, CURLOPT_TIMEOUT, 30);
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
            curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
            curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $res = json_decode(curl_exec($ch));
    
            curl_close($ch);
    
        }

    }
}

class sendNotificationIncident_TestHarness implements RNCPM\ObjectEventHandler_TestHarness {

    static $inc = null;

    public static function setup() {
        $inc2 = new RNCPHP\Incident;
        $inc2->Subject = "Quiq test";
        $contact = new RNCPHP\Contact();
        $contact->Phones = new RNCPHP\PhoneArray();
        $contact->Phones[0] = new RNCPHP\Phone();
        $contact->Name = new RNCPHP\PersonName();
		$contact->Name->First = "Quincy";
		$contact->Name->Last = "QuiqTest";
		$contact->Phones[0]->PhoneType=new RNCPHP\NamedIDOptList();
		$contact->Phones[0]->PhoneType->LookupName = "Home Phone";
		$contact->Phones[0]->Number = "+00008675309";
		$contact->save(RNCPHP\RNObject::SuppressAll);
        $inc2->PrimaryContact = $contact;

        static::$inc = $inc2;
        return;
    }

    public static function fetchObject($action, $incect_type) {
        return(static::$inc);
    }

    public static function validate($action, $inc) {
        return true;
    }

    public static function cleanup() {
        return;
    }

}


