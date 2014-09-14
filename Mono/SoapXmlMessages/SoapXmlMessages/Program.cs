using System;
using System.ServiceModel;
using SoapXmlMessages.www.thomas_bayer.com;

namespace SoapXmlMessages
{
    class BankDataAccessor
    {
        public static void Main (string[] args)
        {
            var accessor = new BankDataAccessor ();
            accessor.GetBankDataByUserInput ();
        }

        public void GetBankDataByUserInput ()
        {
            Console.Write ("Bitte geben Sie ihre Bankleitzahl ein: ");
            var blz = Console.ReadLine ();
            try {
                PrintBankDetails (GetBankByBankleitzahl (blz));
            } catch (InvalidOperationException ex) {
                Console.WriteLine (ex.Message);
                Console.WriteLine (ex.InnerException.Message);
            }
        }

        public thomasbayer.com.blz.details GetBankByBankleitzahl (string blz)
        {
            var serviceFactory = new BLZServiceFactory ();
            var client = serviceFactory.CreateServiceFor (this);
            try {
                return client.getBank (blz);
            } catch (System.Web.Services.Protocols.SoapException ex) {
                throw new InvalidOperationException ("Der Webservice hat einen Fehler gemeldet!", ex);
            }
        }

        public void PrintBankDetails (thomasbayer.com.blz.details details)
        {
            Console.WriteLine ("Name: {0}, BIC: {1}, PLZ: {2}, Ort: {3}", 
                details.bezeichnung, details.bic, details.plz, details.ort);
        }

        public void OnSoapXmlActionOccured (object sender, StringEventArgs e)
        {
            // So something with the Request / Response-Messages, logging for example
            Console.WriteLine (e.Xml);
        }
    }

    class BLZServiceFactory
    {
        public BLZServicePortTypeClient CreateServiceFor (BankDataAccessor accessor)
        {
            var messageInspector = new XmlMessageInspector ();
            // bind some simple handling method to just print out the messages.
            messageInspector.SoapXmlRequestOccured += accessor.OnSoapXmlActionOccured;
            messageInspector.SoapXmlResponseOccured += accessor.OnSoapXmlActionOccured;

            // inject our inspector into a concrete behavior
            var messageBehavior = new InterceptMessageBehavior (messageInspector);

            var client = new BLZServicePortTypeClient (new BasicHttpBinding (), 
                            new EndpointAddress ("http://www.thomas-bayer.com/axis2/services/BLZService"));

            // here we can inject an interception object, which itself calls in our case
            // the inspector, that catches the XML Messages and raises the defined events
            client.Endpoint.Behaviors.Add (messageBehavior);

            return client;
        }
    }
}
