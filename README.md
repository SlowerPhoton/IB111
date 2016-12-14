# IB111

<b>Prisonner's Dilemma</b>

Simulation of gameplay of different strategies for this game. 

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

<b>Resize</b>



