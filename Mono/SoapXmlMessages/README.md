================================================================================
Accessing the generated XML of SOAP requests and responses in .NET made "simple"
================================================================================

(Or: a ballad of chasing lame SOAP XML access in four acts)
------------------------------------------------------------

SOAP dropped its [acronym](http://en.wikipedia.org/wiki/SOAP#History) long time 
ago - although I had always the impression, that SOAP is a complex beast like C++, 
now it is clearer than ever to me, why that was a good and consequent move!

It's quite **simple**: SOAP is not simple, instead it is daunting and cumbersome!

Of course good tooling can, should, even better must and - in fact - does 
support the developer in implementing SOAP-webservices and clients in C#. But 
almost every task you wanna do besides the straight calling of a service is 
ending up in implementing thousands of interfaces.

Of course it is nice, to follow good patterns and practises (especially in 
static typed languages with a simple object model and single dispatching), 
as it makes a framework and the workflows made with it customizeable. 

But: For common tasks one should provide a built-in standard solution - 
at least in my humble opinion!

Well, Microsoft seems to think *differently*... as we will see.


The "problem"
-------------

If you use a SOAP webservice, you might be interested in knowing, what XML data
is really generated and sent by your application, to be more precise by the
framework, that one uses to deal with SOAP services. 

(**Please ignore all these awful tutorials on the net, where people show how 
to manually craft the XML requests and responses! Use a framework that handles 
that for you!**)

Perhaps you want to make sure, that you send and receive the data you expected
or it is just to document which actions had taken place.

So this really sounds simple and rational, doesn't it?


The "solution"
--------------

In .NET there is a built-in framework located in the `System.ServiceModel`
namespace. In Visual Studio and MonoDevelop - which I used to get things work
under Linux - you have furthermore a tool integrated, that automatically 
generates the needed stubs from a given WSDL file.

That makes calling an existing webservice really easy (I chose the famous
webservice by Thomas Bayer for searching informations about german bank data
as my [example webservice](http://predic8.de/soap/blz-webservice.htm).):

```cs
    // create a stub-object from the generated classes:
    var client = new BLZServicePortTypeClient (
        new BasicHttpBinding (), 
        new EndpointAddress ("http://www.thomas-bayer.com/axis2/services/BLZService")
        );
    
    // and just call an operation
    var result = client.getBank (blz);
    
    // now you can process the properties in the result object
```

Ok, looks simple and straight forwarded. 

But how can we get the request message?
Isn't there something like a `client.RequestMessage`-property? Or perhaps
a super intelligent `ToString`-Method?

Sorry, that would be to easy for the world of SOAP!

As the whole internal process - that is happily a *black box* for the user - is 
surely complex and the developers wanted to keep it as generic and flexible 
as possible, they have provided some hooks within the object model. One might 
know this by the [template method pattern](http://en.wikipedia.org/wiki/Template_method_pattern),
which enables the client to inject custom actions and behaviors into the 
execution process.

**Remark: This is not an evil thing at all!** On the contrary, this is based
upon the [open closed](http://en.wikipedia.org/wiki/Open/closed_principle) 
principle, which is the second basic principle of 
[SOLID](http://en.wikipedia.org/wiki/SOLID_%28object-oriented_design%29).

Ok, after this clearification let's go on...

There is a property `client.Endpoint.Behaviors` that can take arbitrary objects
of the type `IEndpointBehavior`. This interface provides a collection of
different types of hooks, which one can use to intercept the default workflow:

- `AddBindingParameters`
- `ApplyDispatchBehavior`
- `ApplyClientBehavior`
- `Validate`

Our interest lies in the `ApplyClientBehavior`-method! There we can access the
``behavior``-object of a client-runtime-object (that is one, that is only living 
during the execution of a webservice and is not directly accessible before or
after the call of an operation). We can inject a so called *MessageInspector*,
defined by the interface `IClientMessageInspector`:

```cs
    public class InterceptMessageBehavior  : IEndpointBehavior
    {
        // other methods and stuff

        public void ApplyClientBehavior (ServiceEndpoint serviceEndpoint, 
                                         ClientRuntime behavior)
        {
            // inject our custom inspector, that will deal with the messages
            // as we will see in a minute
            behavior.MessageInspectors.Add (new MyCustomMessageInspector());
        }
```

What does an inspector look like? Well that is quite a simple interface, with
just two methods to implement: One that is accessed just *before* sending
the request and one that is accessed just *after* getting the response.

Think of this as the place to provide your own kind of 
[strategy](http://en.wikipedia.org/wiki/Strategy_pattern), that the 
process should handle at some point during its execution.

So the implementation of that interface will be finally our playground 
to get the "goddamn" XML of the SOAP messages:

```cs
    public class XmlMessageInspector : IClientMessageInspector
    {
        public void AfterReceiveReply (ref System.ServiceModel.Channels.Message message, 
                                    object correlationState)
        {
            Console.WriteLine(message.ToString());
        }

        public object BeforeSendRequest (ref System.ServiceModel.Channels.Message message, 
                                        System.ServiceModel.IClientChannel channel)
        {
            Console.WriteLine(message.ToString());
            return null;
        }
    }
```

Wow! There at least we have a ``ToString``-Method, that gives us the much
longed-for XML string :-)

The last thing we have to do, is to tell our client, that we have a super
self made custom client behavior, that it should gently call during the
execution of a SOAP operation.

```cs
    client.Endpoint.Behaviors.Add (new InterceptMessageBehavior());
```

And - tadaaaaaa - we have allready reached the end of our *quest*. Just fire up
the request and see the beauty of the prefectly shaped SOAP XML strings... 😍


The "rant"
----------

Well, we had to implement just two interfaces, not "thousands", and they were
even not very complex and fit nicely into the 
[interface segregation principle](http://en.wikipedia.org/wiki/Interface_segregation_principle).
So everything is fine, the world of SOAP pacified and I am just happy?

Of course **NOT**! 😠

I have no problem in general with these design decisions to expose a clear and 
distinguished interface for hooking into a workflow and probably manipulate it,
as the .NET framework provides it for us here.

But why on earth did they not provide a **default** implementation for such
common tasks? Sorry, but you can't tell me, that none of the core developers
never faced this kind of problem! And even if they never ever considered that
to be a common problem, why they did not listen to the users and handed it in
later on? Just search for it on google and you will **recognize** that 
this **is** a common problem!

The usage of patterns and ways to open up a workflow process for extensions is
important and a good thing. Not to provide **default** solutions to make
common tasks easy and simple, is a **bad** thing!


The end
-------

So, now I calm down and say a few concluding and constructive-minded thoughts 
about my solution.

As C# provides a built-in support for the observer pattern, I decided to use
events to provide a loose coupling between the webservice and the backend logic.
You just have to pass an arbitrary listener into the creation process of a 
service client, which you can easily put into some kind of factory or builder.

In my example application you will find the construction process in the
`BLZServiceFactory`-class.

Imho it is not a big deal to provide something similar within the .NET 
framework... that would save so much life-time that you can spend with much 
nicer things than to explore the possibilities of dealing with SOAP
problems... ok, almost everything is more fun than SOAP 😉 

(Perhaps that is the reason, why the .NET developers did not spend too much 
time to polish their SOAP framework? 😈 just kidding... )


P.S.
----

If you like my thoughts and solution, tell it to the world and Microsoft; if
you dislike it, tell it to **me**!

Hey guys @Microsoft: Feel free to grab my solution and put it into the 
framework (see the license-file with the BSD license)! 
Please help people wasting less time in the future! 😛


P.P.S.
------

I excuse for the unconvenient formating of the source code - MonoDevelop seems
to handle that differently than Visual Studio does. In my opinion it is
quite ugly, because it looks like a mixture of Java and C# as we know it.
Spaces before methods are just misleading as they remind one on collection
literals that one might know from other languages like Python or Clojure.

Perhaps there are options in MonoDevelop to correct these issues, but to be
honest I have no motivation to get into it further more. C# is good for work,
but not enough fun for my sparetime 😃
