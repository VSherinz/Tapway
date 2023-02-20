The idea of this project is to showcase event driven architecture.

Entity involved is: Producer, Messaging Queue and Consumer.

Hard Dependency
1. Docker Daemon (Docker Desktop)

Instruction
1. Clone project from git
2. Open via IDE of choice
3. On root of project (Where docker-compose is located)
4. Run command -> 'docker-compose up -d --build' to create image and run the container


Instruction Part 2
1. Trigger Producer endpoint called push_footage(body: JsonString)
2. There are two ways of triggering this at the moment
   1. Postman tool with raw json payload triggering the api
   2. newman CLI to trigger API based on saved single seed

Using Docker Desktop (or CLI equivalent)
1. Click Containers tab (on the left)
2. Under the list of available container, our 3 running container are grouped according to compose definition
3. Click on small > dropdown beside Tapway
4. The dropdown list will show list of container as specified by both our dockerfile and docker-compose
5. user can look into the running container by clicking any white area along the container row
6. Do 5) for FootageProducer
7. In the navigated UI, user will be able to see logs implemented along with terminal to navigate through the working directory of the application

Structure of container (Consumer will only have Consumer subdirectory and vice versa):

    app
        Consumer
            src
                logging.yaml (logging config)
                main.py (main logic aka entrypoint)
        Producer
            src
                logging.yaml (logging config)
                main.py (main logic aka entrypoint)
                models
                    FootageBody (pydantic model for API validation)
    tmp
        Producer
           (list of log available)
        Consumer
           (list of log available)

Flow of the application
1. docker-compose will build image, compose and run according to definition provided in dockerfile and docker-compose
2. All 3 container will run (consumer will have 20sec sleep to ensure it is the last)
3. Producer will have their definition of publish channel (via pika)
4. Consumer will have their definition of subscribe channel (via pika)
5. Upon Producer endpoint being triggered with fully validated data, it will send the message to published channel 
6. Upon available data in the published channel that consumer subscribed to, it will wake and convert the data back into dictionary
7. Footage data formed from 6) will then be used to produce CSV according to understanding of requirement
8. CSV produced are called 'output.csv' and it is located in Consumer container at [app/Consumer/src/output.csv]