# Our Project
The 2024 FRC game, Crescendo, was home to many unforeseen upsets where statistics and prediction models proved no match for strategic masterpieces from seemingly underpowered alliances. For us, this sentence carries some salt having recently lost the World Championship in convincing fashion to an alliance that was predicted to lose every match on Einstein. This observation led us to the question: Do certain FRC games foster upset-prone playoff brackets?

## Constructing Hypotheses
While the above question motivates the steps to follow, it lacks specificity on exactly what we want to measure. To establish a clear direction, we state the following null and alternative hypotheses for each FRC game from the last five years:

**Null Hypothesis:** The outcomes of playoff brackets from this game do not significantly deviate from the expected bracket outcomes. <br/>
**Alternative Hypothesis:** The outcomes of playoff brackets from this game do significantly deviate from the expected bracket outcomes.

## Procedural Design
The end goal is to conduct a 1-sample $z$-test for the population proportion of upset brackets to determine if a specific game is upset-prone. But first, we must operationally define what an upset bracket is and devise a methodology for collecting data on such brackets. We start with the first task:

**Upset Bracket:** An upset bracket is a bracket whose final rankings have a cumulative probability of less than 50% occurrence. In other words, of all possible bracket outcomes, if the sum of all probabilities of brackets less extreme than the one that occurred is 50% or more, we consider the bracket to be an upset.

### The Probability

There are two levels to designing a probability model suitable for evaluating brackets:

**Match Probability:** We must be able to take any two alliances from a playoff bracket and determine the probability of each winning based on readily available metrics. Even if the two alliances never played each other in a real match, the outcome of a hypothetical match between the two is important in determining the next step. <br/>
**Bracket Probability:** With match probabilities between any two alliances known, we need a way to simulate each bracket outcome and create a distribution to compare the event's final rankings with.

To calculate the outcome probability between any two hypothetical alliances, we utilize the EPA (expected points added) metric and average qualification match scores for each team in an alliance. For simplicity, we assume that alliances only play with their first three teams if a fourth exists via a backup bot or through an alliance structure in a championship event. How we derive match probability is as follows:
1. Calculate the expected score of an alliance. For this, we simply sum the EPAs of the teams in the alliance:
```
for team in alliance.teams:
  AVG_SCORE += team.EPA
```
2. Calculate the standard deviation of an alliance's expected score. This one was a bit more complicated, but the math performed is below:
```
for team in alliance.teams:
  VAR_SCORE += pow(team.EPA / team.AVG_QUAL_SCORE, 2) * pow(team.SD_QUAL_SCORE, 2)
SD_SCORE = math.sqrt(VAR_SCORE)
```
3. Run 1000 simulations of a hypothetical matchup and return the probability of the match outcome.

Now, 
