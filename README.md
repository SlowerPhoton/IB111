# IB111

<b>Prisoner's Dilemma</b>

Simulation of gameplay of different strategies for this game. 

Strategies used:
<ul>
<li> 
class: <b>RandomChoice</b>
<p>
1/2 chance of cooperating, 1/2 of defecting
<p>
</li>
<li> 
class: <b>Cooperative</b>
<p>
Cooperate until the opponent defects, then defect a random amount of turns and attempt to cooperate again.
<p>
</li>
<li> 
class: <b>RealPlayer</b>
<p>
Enables the user to play.
<p>
</li>
<li> 
class: <b>AlwaysAccept</b>
<p>
Always cooperate.
<p>
</li>
<li> 
class: <b>AlwaysRefuse</b>
<p>
Always defect.
<p>
</li>
<li> 
class: <b>TitForTat</b>
<p>
Mimic opponent's last decision. (The first turn is completely random.)
<p>
</li>
<li> 
class: <b>Adaptive</b>
<p>
Attempt to guess the class of the opponent. Aside form the mentioned classes also recognizes Forgiving/Unforgiving Pavlov. Use weaknesses of the class against the opponent.
<p>
</li>
</ul>

<p> <img src="http://i.imgur.com/BhW1IoJ.png" /> </p>
<p> <a href="http://i.imgur.com/BhW1IoJ.png">Here are results of a battle of all strategies. </a></p>

<b>Beat Analysis</b>

In this project I focus on finding beats in wave files. 

There are three main strategies to find it:
<ul>
<li> 
<b>
Amplitude 
</b> 
<p>
Look for samples with bigger apmlitude than a certain threshold.
</p>
<p>
<i>method:</i> amplitude 
</p>
<p>
<i>rating:</i> Good for rock, pop songs and computer-generated music, nearly useless for singer-based songs, useless for classical music/metal 
</p>
</li>

<li> 
<b>
Difference between adjacent samples
</b>
<p>
Look for samples with bigger difference than a certain threshold.
</p>
<p>
<i>method:</i> difference 
</p>
<p>
<i>rating:</i> Great for computer-generated music, good for rock and pop songs, nearly useless for singer-based songs, useless for classical music/metal 
</p>
</li>

<li> 
<b>
Curvature of a continuous block of samples 
</b>
<p>
Look for blocks with curvature higher than a certain threshold.
</p>
<p>
<i>method:</i> curvature 
</p>
<p>
<i>rating:</i> Great for computer-generated music, good for rock, pop and singer-based songs, nearly useless for classical music/metal 
</p>
</li>
</ul>

<p> An idea to make a hash of a certain block to represent its shape proved to be completely useless and extremely slow.</p>

<p> You can find a google presentation about this project <a href="https://docs.google.com/presentation/d/1MXV2jDWGclThWqRjNi5Ju1d4tXH6MN4FX6jf2mSPa1E/edit?usp=sharing"> here</a>. 
</p>

<b>Resize</b>

<p>
Method <i>naive_enlarge</i> expands an image by repetition. Twice as large image thus gets each column and row duplicated. </p>
<p>
Method <i>naive_shrink</i> shrinks an image by collapsing multiple rows/columns into one (with arithmetic mean). Other approaches seem to work worse. 
</p>
<p>
The main "universal" method <i>resize</i> makes use of the mentioned functions, being able to transform an image to any resolution. However, there is a lot left for optimization.   
</p>
<p>
<b>Show-off</b><br>
<div>
<img src="http://i.imgur.com/4NudilW.jpg" /><br>
1920 x 1080
</div>
<div>
<img src="http://i.imgur.com/xhwsJTS.png" /><br>
540 x 540
</div>
<div>
<img src="http://i.imgur.com/JCYWcnG.png" /><br>
540 x 480
</div>
</p>
