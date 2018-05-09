
CAU Capston Design CAUCVS Team git repository

Our Data and Code.

#CAUCVS


How to build

first. 

        Install the Anaconda
        
        pip install TensorFlow.
        pip install numpy
        ...( if any message you have to write more command)
        
seoncd. 

        write a command
        
        like that
        
        pytone (codename) (-- {option parser}) (option name) = (address)  ..
      
        if you don't have any option, you can not use -- comand
        
        but in this project we need minimum 6 option.
        
        bottlenect_dir option ( directory of  bottlenect address) 
        model_dir  option     ( directory of model address      )
        output_graph option   ( output graph address            )
        output_labels option  ( output label address            )
        image_dir option.     ( input image directory address   )
        how_many_training_steps option. ( Number of time to CNN algoritm )
        
         command of  this project.
        
          python retrain.py --bottleneck_dir=./workspace/bottlenecks --model_dir=./workspace/inception --                 output_graph=./workspace/flowers_graph.pb --output_labels=./workspace/flowers_labels.txt --image_dir ./workspace/flower_photos --how_many_training_steps 1000
        
          
