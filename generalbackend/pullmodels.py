from huggingface_hub import HfApi, list_models #ModelSearchArguments
api = HfApi()
models = api.list_models()
#newModel = ModelSearchArguments()
counter = 0
for model in models: 
    if counter <50:
        print(model.modelId)
        counter +=1
    else: 
        break