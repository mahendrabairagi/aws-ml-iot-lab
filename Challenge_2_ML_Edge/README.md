# Challenge 2: ML at the Edge
## Summary

Now that we've successfully built out a pipeline for our application based around cloud-inference, it's time to revisit this configuration. In ML/IoT pipelines, we often have a choice to make about where inference is ran. Recall that in this particular scenario, the face detection inference is acting as a gate to the Rekognition API call:
* Only trigger when a face is detected
* Only actually send the face crop

In the previous Challenge, we cited performance and speed as two advantages of cloud inference. Unfortunately, by keeping inference in the cloud our IoT devices must regularly send images at constant intervals (i.e. they're **always on**) and they send entire images. This seems like a waste of bandwidth; by putting face-detection inference at the edge, we can directly make Rekognition calls from the device itself. The tradeoff here is that while we're only sending face crops when there detected over the network, inference at the edge can be less performant.

In this challenge, you will swap out the ML/IoT part of the previous pipeline with a new pipeline that uses AWS DeepLens to run inference on the edge. DeepLens will then put face crops to the S3 bucket correctly, continuing the rest of the application pipeline.

* Step-by-step instructions (re:screenshots)
* Instructions on re-setting and registering DeepLens
* configure inference lambda for edge inference w/ S3 bucket
* Deploy lambda, model as a DeepLens Project to device

## Instructions

### AWS DeepLens Registration

[Instructions on registering DeepLens can be found here.](https://s3.amazonaws.com/deeplens-workshop-06-20-2018/MLGGDeepLensWorkshop06-20-2018.pdf)

### Create DeepLens Lambda

Now that you've registered your DeepLens device, it's time to create a custom project that we can deploy to the device to run face-detection and push crops to S3.

A DeepLens **Project** consists of two things:
* A model artifact: This is the model that is used for inference.
* A Lambda function: This is the script that runs inference on the device.

Before we deploy a project to DeepLens, we need to create a custom lambda function that will use the face-detection model on the device to detect faces and push crops to S3.

You will repeat the steps in Challenge 1 where you created a Lambda function from the "greengrass-hello-world" blueprint. This time, however, you will select "Choose an existing role" and then select "AWSDeepLensLambdaRole". 

![Alt text](../screenshots/deeplens_lambda_0.png)

Next, you will replace the default function with the [inference-lambda.py](https://github.com/mahendrabairagi/aws-ml-iot-lab/blob/master/Challenge_2_ML_Edge/inference-lambda.py) script under Challenge_2.

**Note**: Be sure to replace "your bucket" with the name of the bucket you've been using thus far.


Once you've copied and pasted the code, click "Save" as before, and this time you'll also click "Actions" and then "Publish new version".

![Alt text](../screenshots/deeplens_lambda_1.png)

Then, enter a brief description and click "Publish."

![Alt text](../screenshots/deeplens_lambda_2.png)

Before we can run this lambda on the device, we need to attach the right permissions to the right roles. While we assigned a role to this lambda, "AWSDeepLensLambdaRole", it's only a placeholder. Lambda's deployed through greengrass actually inherit their policy through a greengrass group role.

Similar to what we did in challenge 2, we need to add permissions to this role for the lambda function to access S3. To do this, go to the IAM dashboard, find the "AWSDeepLensGreenGrassGroupRole", and attach the policy "AmazonS3FullAccess". If you've forgotten how to do this, please refer to Challenge 2 as an example.

### Create & Deploy DeepLens Project

With the lambda created, we can now make a project using it and the built-in face detection model.

From the DeepLens homepage dashboard, select "Projects" from the left side-bar:

![Alt text](../screenshots/deeplens_project_0.png)

Then select "Create new project"

![Alt text](../screenshots/deeplens_project_1.png)

Next, select "Create a new blank project" then click "Next".

![Alt text](../screenshots/deeplens_project_2.png)

Now, name your deeplens project.

![Alt text](../screenshots/deeplens_project_3.png)

Next, select "Add model". From the pop-up window, select "deeplens-face-detection" then click "Add model".

![Alt text](../screenshots/deeplens_project_4.png)

Next, select "Add function". from the pop-up window, select your deeplens lambda function and click "Add function".

![Alt text](../screenshots/deeplens_project_5.png)

Finally, click "Create".

![Alt text](../screenshots/deeplens_project_6.png)

Now that the project has been created, you will select your project from the project dashboard and click "Deploy to device".

![Alt text](../screenshots/deeplens_project_7.png)

Select the device you're deploying too, then click "Review" (your screen will look different here).

![Alt text](../screenshots/deeplens_project_8.png)

Finally, click "Deploy" on the next screen to begin project deployment.

![Alt text](../screenshots/deeplens_project_9.png)

You should now start to see deployment status. Once the project has been deployed, your deeplens will now start processing frames and running face-detection locally. When faces are detected, it will push to your S3 bucket. Everything else in the pipeline remains the same, so return to your dashboard to see the new results coming in!

**Note**: If your model download progress hangs at a blank state (Not 0%, but **blank**) then you may need to reset greengrass on DeepLens. To do this, log onto the DeepLens device, open up a terminal, and type the following command:
`sudo systemctl restart greengrassd.service --no-block`. After a couple minutes, you model should start to download.
