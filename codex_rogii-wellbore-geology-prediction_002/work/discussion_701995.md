╭─ Is the public LB test set (26%) fixed?  ────────────────────────────────────╮
│ Author: Alhasan Abdellatif | Votes: 7 | Comments: 13 | Created: 2026-05-20   │
│ https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction/discus │
│ sion/701995                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯


▌ This leaderboard is calculated with approximately 26% of the test data. The 
▌ final results will be based on the other 74%, so the final standings may be 
▌ different.                                                                  

I have noticed that running & submittin the same exact notebook, same trained   
models, gives very different score with differences reaching over ~ 0.5 ft.     
what does this mean? Is the public LB test set (26%) fixed?                     

── 13 Comments ──

PatrickAIForFun 2026-05-20
This most likely means that not all randomness is fixed within your notebook    
(sometimes, even fixing all random seeds is not deterministic when using the    
GPU). The 26% public split is fixed (not a host - thus can't confirm 100% but it
wouldn't make sense to vary it and I don't know of any competition where this   
would have been the case).                                                      

PC Jimmmy 2026-05-20
As noted by PatrickAIForFun - the test has never varied in the 8 years I have   
been here.                                                                      

Not sure I understood your difference value - what is the smallest and largest  
score you have for what you believe was the exact same notebook?                

Alhasan Abdellatif 2026-05-20
Completely agree. It does not make sense if it vaires. I will double check the  
randomness in the notebook. Thanks!                                             

Alhasan Abdellatif 2026-05-20
For example, copying and re-submitting this top scored public notebook          
https://www.kaggle.com/code/nihilisticneuralnet/9-251-rogii-wellbore-geology-pre
diction-dwt-based/notebook led to a 9.724 which is around 0.5 ft difference than
its recorded score 9.251, also another submission scored 9.962. This also       
happens with some of my own notebooks. I will double check the randomness and   
see. Thanks!                                                                    

PC Jimmmy 2026-05-21
Copied and re-submitted the notebook and will let you know in few hours how it  
scored for me.  But as noted results do vary even with a very detailed seed, but
0.5 does seem a bit on the high side.  I would assume that kaggle might be      
running your code on different data center than mine.                           

Zhenyu Zhang ▲-1 2026-05-21
I think it is not fixed                                                         

Radmir Zosimov 2026-05-21
I had the same issue, it’s most likely your feature generation includes         
randomness, fix your seed. Also if you use numba seed has to be set inside a    
function                                                                        

PC Jimmmy ▲1 2026-05-21
WOW - I did even worse at 10.146.                                               

PC Jimmmy 2026-05-21
My LGB model rmse values match the posted original code. My Catboost values also
match the posted orginal code. My Running Hill Climbing values match. My        
predicted values for the fake test data don't match - 11747.366412 vs           
11747.366702 for the very first for example.                                    

This seems more like a code error/omission rather than a seeding issue.         

YtLiu 2026-05-22
The test set should be fixed. The score discrepancy you’re experiencing is most 
likely due to randomness in your code not being fully controlled. Multi-process 
parallelism and GPU usage can both introduce randomness. Additionally, if you’re
using Numba for acceleration, the seed set at the Python level won’t be         
propagated to the functions compiled by Numba. When I tried to completely       
control the randomness, the scores for the two submissions were consistent.     

PC Jimmmy 2026-05-22
In the original notebook that you forked the code from there is a comment from  
at least one other person who got a different value despite using the exact     
code.                                                                           

Hamza 2026-05-23
I run my same LGB Baseline 2 times, 1st time I got score of 9.964 and Second    
time I got the score 9.477                                                      

Chris Deotte ▲4 2026-06-05
The test data does not change.                                                  

The reason our scores change is because many feature engineering are stochastic 
in this competition. Feature engineering is the process of us making new columns
on the train and test data. So every time we submit our notebook, the train.csv 
will be different and the test.csv will be different because when we add our    
features they are different (stochastic) each time.                             

(And train.csv affects the trained model and test.csv affects the inference of  
the model)                                                                      

