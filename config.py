#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    QNA_KNOWLEDGEBASE_ID = os.environ.get("QnAKnowledgebaseId", "/knowledgebases/e229d654-168a-440f-a9db-8d01c984826b/generateAnswer")
    QNA_ENDPOINT_KEY = os.environ.get("QnAEndpointKey", "024e013b96d442f4ac020e63662eaf4e")
    QNA_ENDPOINT_HOST = os.environ.get("QnAEndpointHostName", "https://universalrentals.cognitiveservices.azure.com/qnamaker/v5.0-preview.1")

