# Dolores Diaries

These are the Dolores Diaries, a personal log of the development of the Dolroes R2 project for personal use.

## March, 19th 2019

## Webpack vs Parcel

Parcel looks really fast but the Webpack support in the plugins, docs, etc. is really compelling. I'll stick with Webpack, at least for now.

### Bootstrap a new Serverless service

Created a brand new Serverless project using the [aws-nodejs-typescript](https://github.com/serverless/serverless/tree/master/lib/plugins/create/templates/aws-nodejs-typescript) template provided by the project itself:

```bash
$ serverless create --template aws-nodejs-typescript
Serverless: Generating boilerplate...
 _______                             __
|   _   .-----.----.--.--.-----.----|  .-----.-----.-----.
|   |___|  -__|   _|  |  |  -__|   _|  |  -__|__ --|__ --|
|____   |_____|__|  \___/|_____|__| |__|_____|_____|_____|
|   |   |             The Serverless Application Framework
|       |                           serverless.com, v1.39.1
 -------'

Serverless: Successfully generated boilerplate for template: "aws-nodejs-typescript"
Serverless: NOTE: Please update the "service" property in serverless.yml with your service name
```
