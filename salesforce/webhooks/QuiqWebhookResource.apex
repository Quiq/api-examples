@RestResource(urlMapping='/quiq/*')
global without sharing class QuiqWebhookResource {
    
    global class QuiqCustomer {
        global String firstName;
        global String lastName;
        global String email;
        global String phoneNumber;
    }
    
    global class QuiqEntity {
        global String type;
        global String id;
    }
    
    global class QuiqConversationEvent {
        global QuiqEntity triggeredBy;
        global Long timestamp;
        global String type;
    }
    
    global class QuiqAsset {
        global String assetId;
        global String contentType;
    }
    
    global class QuiqPlatformData {
        global String tenantPhoneNumber;
    }
    
    global class QuiqLinkImage {
        global String url;
    }
    
    global class QuiqLink {
        global String title;
        global String url;
        global QuiqLinkImage image; 
    }
    
    global class QuiqMessage {
        global String id;
        global String sourcePlatform;
        global String author;
        global Boolean fromCustomer;
        global Long adaptiveTime;
        global String text;
        global Long timestamp;
        global QuiqAsset[] assets;
        global QuiqPlatformData platformData;
        global QuiqLink[] links;
    }
    
    global class QuiqMetrics {
        global Long initialAgentResponseDuration;
        global Long initialAgentResponseDurationSinceAssignment;
        global Long averageAgentMessageDuration;
        global Long averageCustomerMessageDuration;
        global Double averageResponseTime;
        global Long timeToFirstResponse;
        global Integer numberOfAgentMessages;
        global Integer numberOfCustomerMessages;
        global Integer numberOfSystemMessages;
        global Integer numberOfAcceptedTransfers;
        global Integer numberOfRequeues;
        global Integer numberOfResponseTimerExpirations;
        global Long workTime;
    }
    
    global class QuiqIntegration {
        global String provider;
        global String name;
        global String id;
    }
    
    global class QuiqCollaboration {
        global String id;
        global QuiqConversationEvent[] events;
        global QuiqMessage[] messages;
        global Long startTime;
    }
    
    global class QuiqConversation {
        global String id;
        global String status;
        global String owner;
        global String customerPlatform;
        global String customerHandle;
        global QuiqCustomer customer;
        global String contactPointId;
        global String endpointId;
        global QuiqCollaboration collaboration;
        global QuiqConversationEvent[] events;
        global QuiqMessage[] messages;
        global QuiqMetrics metrics;
        global QuiqIntegration[] integrations;
        global Map<String, String> integrationsData;
        global Long startTime;
        global Long endTime;
        global String queue;
    }

    @HttpPost
    global static void acceptData(QuiqConversation data, String eventType, String id, Long timestamp)
    {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        // Ensure that the callers of this API are Quiq 
        // This is an example of security. You should consider storing the secret in a safer location than hashed in APEX code
        String hashedSecret = 'bd8b0b8028f0c34f61712a3c5f83b38b0e75dfd6';
        String hashedInput = EncodingUtil.convertToHex(Crypto.generateDigest('SHA1',Blob.valueOf(req.headers.get('X-Centricient-Hook-Token'))));

        if (hashedInput == hashedSecret) {
          if (data.status == 'closed') {
            QuiqConversation__c convo = new QuiqConversation__c();

            convo.averageAgentMessageDuration__c = (Double)data.metrics.averageAgentMessageDuration / 1000.00; //Divide by 1000 to convert from milliseconds into seconds.
            convo.id__c = data.id;
            convo.NAME = data.id;
            convo.owner__c = data.owner;
            insert convo;
          }
          res.statusCode = 200;
        }
        else {
          res.statusCode = 401;
        }
    }
}
