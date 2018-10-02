public class SendNotification {
    @InvocableMethod(label='Send Notification' description='Sends a notification in Quiq.')
    public static List<ID> doSend(List<Contact> contacts) {
        Contact c = contacts.get(0);
        sendSMS(c.Phone, c.Balance__c);
        return new List<ID>();
    }
    
    @future(callout=true)
    private static void sendSMS(String phoneNumber, Decimal balance) {
        Http http = new Http();
        HttpRequest request = new HttpRequest();

        quiqSettings__c settings = quiqSettings__c.getOrgDefaults();
        
        Blob headerValue = Blob.valueOf(settings.quiqTokenId__c + ':' + settings.quiqTokenSecret__c);
        String authorizationHeader = 'Basic ' + EncodingUtil.base64Encode(headerValue); 

        request.setEndpoint(settings.quiqUrl__c + '/api/v1/messaging/platforms/SMS/send-notification');
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setHeader('Accept', 'application/json');
        request.setHeader('Authorization', authorizationHeader);

        request.setBody('{ "handle": "' + phoneNumber + '", "contactPoint": "$YOUR_QUIQ_CONTACT_POINT", "message": {"text": "$THIS_IS_THE_EXAMPLE_REPLACE_ME This is an automated message. Hello, you currently have a low balance of: ' + balance + '" }}');
        HttpResponse response = http.send(request);

        if (response.getStatusCode() != 201) {
            System.debug('The status code returned was not expected: ' +
            response.getStatusCode() + ' ' + response.getStatus());
        } else {
            System.debug(response.getBody());
        }
    }
}
