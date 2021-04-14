# LayerRemapping Progress

## Goal

The goal of it is to make node 1 move NUM_MOVING_LAYER(i.e. 3) layers to node 0 dynamically during the training process.

So if node 0 trains Layer 0-11 and node 1 trains Layer 12-23 when the program starts. After remapping event triggers, node 0 trains 0-14, and node 1 trains 15-23. 



## What has been done

Transfer of model and Forward Pass should be Okay(not saying they are perfectly done). Backward is not completed.

## Change Note (if you'd like to continue what I have done so far)

1. I tried my best to mark "**# REMAPPING**" on the code section I have made change. (definitely may miss something)

   check "**runtime/engine**" "**runtime/pipe/engine.py|module.py|schedule.py**"

   Also I created "**runtime/pipe/coord_comm.py|simple_coord_server.py**" for simple distributed data store. You have to run an instance as coord server. 

   ```bash
   python3 runtime/pipe/simple_coord_server.py
   ```

   **runtime/pipe/constant.py** stores some constants I used. You can definitely pass them as arguments. This is just a lazy way.

2. **simple_coord_server.py** serves as master node for torch distributed value store. The code should be simple to understand.  Read this https://pytorch.org/docs/stable/distributed.html#distributed-key-value-store. 

3. In **schedule.py**

   I created **RemapCheck**, **RemapExec** instruction class (line 487) and append these command in training step (line 209). 

   (just search *# REMAPPING*)  

4. In **pipe/engine.py**

   1st *\# REMAPPING*: line 222

   **buffer_to_mbatch** is a variable to store mapping of ***pipe_buffer_id*** to ***micro_batch_offset***

   **remapping_due** is a variable to indicate if there is remapping happening

   **CoordComm** is class for getting/setting remapping_due, transferring tensors/model parameters. *The implementation of this TCP Store thing is for quick prototype.

   

   2nd *\# REMAPPING*: line 577

   set  **buffer_to_mbatch**, should be intuitive

   

   3rd  *\# REMAPPING*: line 623 /  4th  *\# REMAPPING*: line 683

   func **mark_mbatch_backward_finished** mark  n*th* micro_batch on this stage is done (for recomputation purpose). 

   Think this. When remapping happens, if node *1* has compute its forward pass, should I pass the fwd result to node *0* ?  I decide to make node 1 recompute the forward because I couldn't find any solution on the Internet that let you run backward on a different machine. And in theory, the number of mbatch that requires fwd recomputation should not be large. I guess it is ~ # of pipeline stages.

   

   5th *\# REMAPPING*: line 1254

   **exec_remapping_check/exec_remapping_procedure** are the actual functions to implement the pipeline instruction.

   

   6th *\# REMAPPING*: line 1288 (self explanatory) 

   7th *\# REMAPPING*: line 1319

   **remapping_layer** is function implementing the layer shifting between tow nodes. It transfers **recomputation list** and **state_dict of moving layers**

5.  In **runtime/pipe/module.py**

   1st # REMAPPING: line 93 

   **PartialPipeModule** is a class that holds the new layers gotten transfered. Most of its code are copied directly from **PipelineModule**.

   

   2nd # REMAPPING: line 301 (self explanatory) 

   3rd # REMAPPING: line 451

   compute forward if there are partial_modules

   4th # REMAPPING: line 727

   helper function of moving layers

## TODO

Debug why this code doesn't work

TieredLayer, seed_layers are not handled

Check if gradients are accumulated after state_dict is transferred too

