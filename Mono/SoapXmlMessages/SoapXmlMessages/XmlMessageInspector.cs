using System;
using System.ServiceModel.Dispatcher;
using System.ServiceModel.Description;

namespace SoapXmlMessages
{
    public class StringEventArgs : EventArgs
    {
        public string Xml { get; set; }

        public StringEventArgs (string xml)
        {
            Xml = xml;
        }
    }

    /// <summary>
    /// <remarks>>
    /// Think of this hook-object a as "strategy" or "command" that will be integrated at some point
    /// of the execution-process of a webservice.
    /// </remarks>
    /// </summary>
    public class XmlMessageInspector : IClientMessageInspector
    {
        /// <summary>
        /// Occurs when a SOAP request message is available
        /// </summary>
        public event EventHandler<StringEventArgs> SoapXmlRequestOccured;

        /// <summary>
        /// Occurs when SOAP response message is available
        /// </summary>
        public event EventHandler<StringEventArgs> SoapXmlResponseOccured;

        public void AfterReceiveReply (ref System.ServiceModel.Channels.Message message, 
                                    object correlationState)
        {
            // here we can finally access the XML by the overloaded ``.ToString``-method
            if (SoapXmlResponseOccured != null) {
                SoapXmlResponseOccured (this, new StringEventArgs (message.ToString ()));
            }
        }

        public object BeforeSendRequest (ref System.ServiceModel.Channels.Message message, 
                                        System.ServiceModel.IClientChannel channel)
        {
            // here we can finally access the XML by the overloaded ``.ToString``-method
            if (SoapXmlRequestOccured != null) {
                SoapXmlRequestOccured (this, new StringEventArgs (message.ToString ()));
            }
            return null;
        }
    }

    public class InterceptMessageBehavior  : IEndpointBehavior
    {
        /// <summary>
        /// field for an interception (hook-) object, that inspects the SOAP messages
        /// </summary>
        private readonly IClientMessageInspector messageInspector;

        public InterceptMessageBehavior (IClientMessageInspector messageInspector)
        {
            if (messageInspector == null) {
                throw new ArgumentNullException ("messageInspector");
            }
            this.messageInspector = messageInspector;
        }

        public void AddBindingParameters (ServiceEndpoint endpoint, 
                                        System.ServiceModel.Channels.BindingParameterCollection parameters)
        {
            // we are not interested in changeing something here
        }

        public void ApplyDispatchBehavior (ServiceEndpoint serviceEndpoint, EndpointDispatcher dispatcher)
        {
            // we are not interested in changeing something here
        }

        public void ApplyClientBehavior (ServiceEndpoint serviceEndpoint, ClientRuntime behavior)
        {
            // here we add one "strategy" for handling SOAP messages
            // MS designed this using the "Template Pattern", so we are able to add a
            // specific behavior that will be called during the execution of webservice.
            behavior.MessageInspectors.Add (messageInspector);
        }

        public void Validate (ServiceEndpoint serviceEndpoint)
        {
            // we are not interested in changeing something here
        }
    }
}
