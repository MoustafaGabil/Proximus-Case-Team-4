# Generative AI

Behind the scenes of your 'cousin' ChatGPT is what we call Generative AI (GenAI), that can create  content—such as text, images, video, audio or software code—in response to a user’s prompt or request.

However, this is not magic. It uses many of the tools/techniques developed by traditional AI methods such as machine learning and deep learning that simulate the learning and decision-making processes of the human brain. 

Where does GenAI fit in the AI landscape? You can think of it as a subset of deep learning with a different goal. 

It leverages generative models, such as generative adversarial networks (GANs), variational autoencoders (VAEs), and transformers to learn from data and generate new samples that exhibit similar characteristics. 

![genAI-within-AI](https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a64c9fb-afaf-46d7-aabc-ca34adb17649_1600x1200.png)


## How does it work?
Similar to the models with built so far, GenAI operates in three main phases:

- Training, to create a foundation model that can serve as the basis of multiple gen AI applications. 

- Tuning, to tailor the foundation model to a specific gen AI application.

- Generation, evaluation and retuning, to assess the gen AI application's output and continually improve its quality and accuracy.

In practice, we are mainly users of these models that have been trained and tuned by larger companies and made accessible to the public.

For example, ChatGPT is a web application that uses generative AI at its simplest level. The rise and popularity of ChatGPT exposed many folks to generative AI, and the power of the other generative models called large language models (LLMs) is, as the name suggests, related to language. OpenAI trained ChatGPT on diverse internet text to produce a human-like conversation.

## GenAI vs. Traditional AI

|Area| Traditional AI| Gen AI 
|---|---|---|
Creation versus prediction|Traditional AI focuses on prediction or classification tasks, identifying what something is or forecasting what will happen next based on existing data. |Generative AI creates new content and outputs that did not exist in the original data.
|Hosting and inference| Relative to generative AI, traditional AI models are less complex and require fewer computing resources, allowing them to run on various hardware, from small edge devices to large cloud clusters and everything in between. This flexibility cloud-to-edge is a huge advantage for enterprises. |Generative models are large and complex; for the most part, they are available only on large cloud compute nodes via an API, which has other advantages, such as the knowledge of the world encoded in these foundational models being available to everyone. |
|Training method| Training methods are less expensive and complex |Generative models require a different method of training (self-supervision and multitask learning), which is longer and much more expensive because of the massive scale of data, model sizes, and computing resources required. The costs and complexity of managing this are enormous|
|Training dataset|  Traditional AI models are typically trained on smaller datasets of labeled data. For example, a discriminative AI model for image classification might be trained on a few thousand labeled image datasets.| Generative AI models are typically trained on large datasets of existing content, For example, a generative AI model for image generation might be trained on a dataset of millions of images. 
|Model complexity| |Generative AI models are often more complex than other types because they need to learn the patterns and relationships in the data to generate new content similar to the existing content.
|Adaptation approach|Traditional AI has no adaptive techniques other than labeling more data and going through a full ML loop of training, deploying, and evaluating. |Generative AI, in contrast, has vast world knowledge. Sometimes, one needs to tailor it to specific needs and tasks or distill internal private and proprietary knowledge; this is done via adaptation.|

## Main Providers
Open-source AI is free to access but may require significant investment in development, maintenance, and training, depending on the complexity of the project. 

Proprietary AI comes with licensing fees but often reduces upfront effort with pre-configured solutions, vendor support, and maintenance included in the cost.

Below you will find an summary of some of the main providers.
![main_providers](https://i2.wp.com/miro.medium.com/v2/resize:fit:700/1*y0mHowsazTM_Q94tlmG5RQ.png?w=700&resize=700,366&ssl=1)


## GenAI types
Generative AI can be grouped into two main categories those based on Large Language Models (LLMs) and Diffusion Models.

![genAI_types](./assets/genai_types.png)

We will explore these in the coming chapters.

## Start Here 
To dive deeper into Generative AI, we recommend starting with these resources.

- [AI Fundamentals Track (DataCamp)](https://app.datacamp.com/learn/skill-tracks/ai-fundamentals)
- [Developing AI Applications Track (DataCamp)](https://app.datacamp.com/learn/skill-tracks/developing-ai-applications)


## Additional Resources 
- [Introduction to GenAI (Microsoft GitHub repo)](https://github.com/microsoft/generative-ai-for-beginners/blob/main/01-introduction-to-genai/README.md)
- [Differences between traditional AI and Gen AI](https://www.geeksforgeeks.org/difference-between-generative-ai-and-traditional-ai/)
- [Best Generative AI Certifications in 2025](https://www.new.datacamp.com/blog/ai-certification)
- [How AI chatbots like ChatGPT or Bard work – visual explainer](https://www.theguardian.com/technology/ng-interactive/2023/nov/01/how-ai-chatbots-like-chatgpt-or-bard-work-visual-explainer)
- [Awesome list of GenAI API's](https://github.com/foss42/awesome-generative-ai-apis)
