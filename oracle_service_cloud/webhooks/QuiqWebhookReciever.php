<?php

namespace Custom\Controllers;
use RightNow\Utils\Framework,
    RightNow\Utils\Text,
    RightNow\Libraries\ResponseObject;

class QuiqWebhookReciever extends \RightNow\Controllers\Base
{
    //This is the constructor for the custom controller. Do not modify anything within
    //this function.
    function __construct()
    {
        parent::__construct();
    }

    public function recieve()
    {
        $secret = 'CHANGE_ME';//TODO - change this to match your secret
        $headers = apache_request_headers();
        if($headers['X-Centricient-Hook-Token'] !== $secret){
            header($_SERVER['SERVER_PROTOCOL'] . ' 403 Unauthorized');
            Framework::writeContentWithLengthAndExit(json_encode(Config::getMessage(END_REQS_BODY_REQUESTS_FORMATTED_MSG)) . str_repeat("\n", 512), 'application/json');
            exit();
        }

        $raw_post = trim(file_get_contents("php://input"));
        $data = json_decode($raw_post, true);
        $conversation = $data['data'];

        if(!$conversation)
        {
            header($_SERVER['SERVER_PROTOCOL'] . ' 400 Bad Request');
            // Pad the error message with spaces so IE will actually display it instead of a misleading, but pretty, error message.
            Framework::writeContentWithLengthAndExit(json_encode(Config::getMessage(END_REQS_BODY_REQUESTS_FORMATTED_MSG)) . str_repeat("\n", 512), 'application/json');
        }

        $conversationId = $conversation['id'];
        
        $roqlResultSet = \RightNow\Connect\v1_3\ROQL::query("SELECT Q.ID from CO.QuiqConversation Q Where Q.conversationId = '$conversationId'")->next();
        
        $existingRecordId = $roqlResultSet->next();
            
        if ($existingRecordId === null) {
            $oscConversationRecord = new \RightNow\Connect\v1_3\CO\QuiqConversation();
        }
        else {
            $oscConversationRecord = \RightNow\Connect\v1_3\CO\QuiqConversation::fetch($existingRecordId['ID'], \RightNow\Connect\v1_3\RNObject::VALIDATE_KEYS_OFF);;
        }

        $oscConversationRecord->conversationId = $conversation['id'];
        $oscConversationRecord->status= $conversation['status'];
        $oscConversationRecord->owner = $conversation['owner'];
        $oscConversationRecord->customerPlatform = $conversation['customerHandle'];
        $oscConversationRecord->customerHandle = $conversation['customerHandle'];
        $oscConversationRecord->contactPointId = $conversation['contactPointId'];
        $oscConversationRecord->queue = $conversation['queue'];

        $oscConversationRecord->save();

        echo('Done');
    }
}

