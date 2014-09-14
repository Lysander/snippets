================================================================================
Accessing the generated XML of SOAP requests and responses in .NET made "simple"
================================================================================

(or: a quest for glory in three acts)

SOAP dropped its [acronym](http://en.wikipedia.org/wiki/SOAP#History) long time 
ago - also I had always the impression, that SOAP is a complex beast like C++, 
now it is clearer than ever to me, why that was a good and consequent move!

It's quite **simple**: SOAP is not simple, instead it is dauting and cumbersome!

Of course good tooling can, should, even better must and - in fact - does 
support the developer in implementing SOAP-webservices and clients, but almost 
every task you wanna do besides the straight calling of a service is ending up 
in implementing thousends of interfaces.

Of course it is nice, to follow good patterns and practises (in static typed
languages with a simple object model and single dispatching), as it makes a 
framework and the workflows made with it customizeable. 

But: For common tasks one should provide a built-in standard solution - 
at least in my humble opinion!

Well, Microsoft seems to think *differently*...


The "problem"
-------------

If you use a SOAP webservice, you might be interested in knowing, what XML data
is really generated and sent by your application. To be more precise by the
framework, that one uses to deal with SOAP services.

Perhaps you want to make sure, that you send and receive the data you expected
or it is just to document which actions had taken place.

So this really sounds simple, doen't it?


The "solution"
--------------

In .NET there is a built-in framework located in the `System.ServiceModel`
namespace. In Visual Studio and MonoDevelop - which I used to get things work
under Linux - you have furthermore a tool integrated, that automatically 
generates the needed stubs from a given WSDL file.

That makes calling an existing webservice really easy (I chose the famous
webservice by Thomas Beyer for seraching informations about german bank data
as my [example webservice](http://predic8.de/soap/blz-webservice.htm).):

```cshap
    // create a stub-object from the generated classes:
    var client = new BLZServicePortTypeClient (
        new BasicHttpBinding (), 
        new EndpointAddress ("http://www.thomas-bayer.com/axis2/services/BLZService")
        );
    
    // and just call an operation
    var result = client.getBank (blz);
    
    // now you can process the properties in the result object
```

Ok, looks simple and straight forward. But how can we get the request message?
Isn't there something like a `client.RequestMessage`-property? Or perhaps
a super intelligent `ToString`-Method?

Sorry, that would be to easy for the world of SOAP!

As the whole internal process, that is a *black box* for the user, is surely
complex and the developers wanted to keep it as generic as possible, they
have provided some hooks within the object model, as one might know it by 
the [template pattern](http://en.wikipedia.org/wiki/Template_method_pattern).

**Remark**: This is not an evil thing at all!

There is a property `client.Endpoint.Behaviors` that can take arbitrary objects
of the type `IEndpointBehavior`. This interface provides a collection of
different types of hooks, which one can use to intercept the default workflow:

- `AddBindingParameters`
- `ApplyDispatchBehavior`
- `ApplyClientBehavior`
- `Validate`

Our interest lies in the `ApplyClientBehavior`-method! There we can access the
``behavior``-object of a client-runtime-object (that one, that is only living 
during the execution of a webservice and not directly accessible before or
after the call of an operation). We can inject a so called *MessageInspector*,
defined by the interface `IClientMessageInspector`:

```csharp
    public class InterceptMessageBehavior  : IEndpointBehavior
    {
        // other methods and stuff

        public void ApplyClientBehavior (ServiceEndpoint serviceEndpoint, 
                                         ClientRuntime behavior)
        {
            behavior.MessageInspectors.Add (new MyCustomMessageInspector());
        }
```

What does an inspector look like? Well that is a quite simple interface, which
just has two methods to implement: One that is accessed just *before* sending
the request and one that is accssed just *after* getting the response.

So that interface will be finally our playground to get the "goddamn" XML of
the SOAP messages:

```csharp
    public class XmlMessageInspector : IClientMessageInspector
    {
        public void AfterReceiveReply (ref System.ServiceModel.Channels.Message message, 
                                    object correlationState)
        {
            Console.Writeline(message.ToString());
        }

        public object BeforeSendRequest (ref System.ServiceModel.Channels.Message message, 
                                        System.ServiceModel.IClientChannel channel)
        {
            Console.Writeline(message.ToString());
            return null;
        }
    }
```

Wow! There at least we have a ``ToString``-Method, that gives us the much
longed-for XML string :-)

The last thing we have to do, is to tell our client, that we have a super
self made custom client behavior, that it should gently call during the
execution of an SOAP operation.

```csharp
    client.Endpoint.Behaviors.Add (new InterceptMessageBehavior());
```

And - tadaaaaaa - we have allready reached the end of our *quest*. Just fire up
the request and see the beauty of the prefectly shaped SOAP XML strings... :-D


The "rant"
----------

Well, we had to implement just two interfaces, not "thousands", and they were
even not very complex and fit nicely into the 
[interface segregation principle](http://en.wikipedia.org/wiki/Interface_segregation_principle).
So everything is fine, the world of SOAP pacified and I am just happy?

Of course **NOT**!

I have no problem in general with these design decisions to expose a clear and 
distinguished interface for hooking into a workflow and probably manipulate it,
as the .NET framework provides it for us here.

But why on earth did they not provide a **default** implementation for such
common tasks? Sorry, but you can't tell me, that none of the core developers
never faced this kind of problem! And even if they never ever considered that
to be a common problem, why they did not listen to the users and handed it in
later on? Just search it on google and you **see** that this is a 
**common problem**!

The usage of patterns and ways to open up a workflow process for extensions is
important and a good thing. Not to provide **default** solutions to made
common tasks easy, is a **bad** thing!

So, now I calm down and say a few concluding and constructive-minded thoughts 
about my solution.

As C# provides a built-in support for the observer pattern, I decided to use
events to provide a loose coupling between the webservice and the backend logic.
You just have to pass a arbitrary listener into the creation process of a 
service client, which you can easily put into some kind of factory or builder.

In my example application you will find the construction process in the
`BLZServiceFactory`.

Imho it is not a big deal to provide something similar within the .NET 
framework... that would save so much life-time that you can spend with much 
nicer things than to explore the possibilities of dealing with SOAP
problems... ok, almost everything is more fun than SOAP ;-)

If you like my thoughts and solution, tell it to the world and Microsoft, if
you dislike it, tell it to **me**!


P.S.
----

Hey guys @Microsoft: I allow you to grab my solution and put it into the 
framework! Please help people wasting less time in the future! :-P
