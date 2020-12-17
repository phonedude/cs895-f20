# Forensics Study 2

Slides also downloaded locally to this repo:

- [ForensicsStudy2.pdf](./slides/ForensicsStudy2.pdf)

## Structure

Tracking Narratives on Election Fraud

Intro:
- 2016 Election Fraud - Russia
History in U.S.:
- Origins of Election Fraud
Examples of Today:
- Sharpiegate
- Everylegalvote.com
- Dead people voting
- #stopthesteal & The Fix Is In

## Developer setup

Current working directory for running any of the provided code is expected to be `src`.

Docker dependencies:

```
docker pull oduwsdl/memgator:latest
docker container run -d --name=memgator-server -p 1208:1208 oduwsdl/memgator server
```
