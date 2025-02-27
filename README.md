This is a negative probability calculator.\
You will need Python and Tkinter to run this.

To run the applet, run negprob.pyw. Running sample.py will do nothing. 

# Explanation
Mathematically, probability can be negative.\
However, there is no real physical interpretation of this, like with negative counts.

Think of it like this:
* You start with 5 apples.
* You sell 8 apples throughout the day (now you have -3 apples).
* You pick 5 apples throughout the day.
* So you end the day with 2 apples.

However, if you do the calculations, there is a step in the calculation
where you have a negative ammount of apples despite that being impossible in real life

We can do a similar thing with probability and this applet lets you look at that and play with it yourself.

# The Applet itself
![negprob-app](https://github.com/user-attachments/assets/f896da75-12c5-486a-8241-5da0f23e078b)

The default combination makes it so that if you check either bit, you find that it is 1.\
However, if you check whether they are equivilant, you find that they are not equal at all.

The reason there is no paradox here is because you can only ask one question on each pair of bits.
It is impossible to determine what both bits are.

Another cool combination is this:\
00: -0.25\
01: 0.25\
10: 0.25\
11: 0.75

This makes it so when checking either bit, it will always be 1, but yet when checking whether they are identical, it is 50-50 whether they are or not.

For more information on this topic, see [Wikipedia's article on negative probability](https://en.wikipedia.org/wiki/Negative_probability)
