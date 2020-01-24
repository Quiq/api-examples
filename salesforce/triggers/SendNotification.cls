public class SendNotification {
    @InvocableMethod(label='Send Notification' description='Sends a notification in Quiq.')
    public static List<ID> doSend(List<Contact> contacts) {
        Contact c = contacts.get(0);
        sendSMS(c.Phone);
        return new List<ID>();
    }
    
    @future(callout=true)
    private static void sendSMS(String phoneNumber) {
        Http http = new Http();
        HttpRequest request = new HttpRequest();

        quiqSettings__c settings = quiqSettings__c.getOrgDefaults();
        
        Blob headerValue = Blob.valueOf(settings.quiqTokenId__c + ':' + settings.quiqTokenSecret__c);
        String authorizationHeader = 'Basic ' + EncodingUtil.base64Encode(headerValue); 

        request.setEndpoint(settings.quiqUrl__c + '/api/v1/messaging/notify');
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setHeader('Accept', 'application/json');
        request.setHeader('Authorization', authorizationHeader);

        String contactPoint = 'default'; //TODO - replace with your contact point
        String topic = 'default'; //TODO - replace with your prefered topic
        String text = 'This is an outbound notification sent through Quiq'; //TODO - replace with your outbound messaging

        request.setBody('{ "contactPoint": "'+contactPoint+'", "topic": "'+topic+'", "notifications": [ {"precedence": [], "searchInfo": {"phoneNumber": "' + phoneNumber + '"}, "messageMap": {"default": {"text": "'+text+'"}} } ] }');
        HttpResponse response = http.send(request);

        if (response.getStatusCode() != 201) {
            System.debug('The status code returned was not expected: ' +
            response.getStatusCode() + ' ' + response.getStatus());
        } else {
            System.debug(response.getBody());
        }
    }
}
