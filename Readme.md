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
2. There are three ways of triggering this at the moment
   1. Postman tool with raw json payload triggering the api
   2. newman CLI to trigger API based on saved single seed
   3. run a curl command
3. As of now, 3) is selected as method of choice.

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

Testing
1. From Docker Desktop, navigate to Container tab
2. From container tab, click the drop down '>' icon on Tapway Container
3. On drop down, click white space on FootageProducer row
4. On UI changed, click Terminal Tab
5. On terminal tab, type 'cd Producer/src' without the literal
6. Type 'sh test.sh' without the literal (this will execute the curl within to trigger Producer endpoint)
7. Type 'cd /./tmp/Producer' without the literal
8. Type ls, use 'cat filename' on debug.log and info.log to see info of flow

Testing part 2
1. Repeat Testing step 1) and 2)
2. Click white space on FootageConsumer row
3. Repeat Testing step 4) and 5)
4. Type 'ls' and we can see 'output.csv'
5. Type 'cat output.csv' to see the content
6. Type 'cd /./tmp/Consumer' without the literal
7. Repeat Testing step 8)

Done