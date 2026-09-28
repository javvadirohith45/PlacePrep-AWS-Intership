from extensions import db
from models.user import User
from models.content import *
from werkzeug.security import generate_password_hash
from urllib.parse import urlparse
from seed.coding_bank import seed_coding_bank

APT_TOPICS = [
('Percentages','percentage'),('Profit & Loss','profit-loss'),('Simple Interest','simple-interest'),('Compound Interest','compound-interest'),('Ratio & Proportion','ratio-proportion'),('Averages','averages'),('Time & Work','time-work'),('Pipes & Cisterns','pipes-cisterns'),('Time, Speed & Distance','time-speed-distance'),('Problems on Trains','trains'),('Boats & Streams','boats-streams'),('Mixtures & Alligation','mixtures-alligation'),('Partnership','partnership'),('Number System','number-system'),('HCF & LCM','hcf-lcm'),('Probability','probability'),('Permutation & Combination','permutation-combination'),('Ages','ages'),('Clocks','clocks'),('Calendars','calendars'),('Data Interpretation','data-interpretation'),('Simplification','simplification'),('Algebra','algebra'),('Geometry','geometry'),('Mensuration','mensuration')]
REASON_TOPICS = [
('Analogy','analogy'),('Number Series','number-series'),('Alphabet Series','alphabet-series'),('Coding-Decoding','coding-decoding'),('Blood Relations','blood-relations'),('Direction Sense','direction-sense'),('Syllogisms','syllogisms'),('Statements & Conclusions','statements-conclusions'),('Statements & Assumptions','statements-assumptions'),('Seating Arrangement','seating-arrangement'),('Puzzles','puzzles'),('Ranking & Order','ranking-order'),('Venn Diagrams','venn-diagrams'),('Classification','classification'),('Odd One Out','odd-one-out'),('Data Sufficiency','data-sufficiency'),('Logical Reasoning','logical-reasoning'),('Non-Verbal Reasoning','non-verbal-reasoning'),('Clocks','reasoning-clocks'),('Calendars','reasoning-calendars')]

COMPANIES = {
'TCS':'https://www.tcs.com/careers','Infosys':'https://www.infosys.com/careers.html','Wipro':'https://careers.wipro.com/','Accenture':'https://www.accenture.com/in-en/careers','Cognizant':'https://careers.cognizant.com/in/en','Capgemini':'https://www.capgemini.com/in-en/careers/','HCL':'https://careers.hcltech.com/go/India/9553955/','Deloitte':'https://www.deloitte.com/global/en/careers.html','Tech Mahindra':'https://careers.techmahindra.com/','Zoho':'https://www.zoho.com/careers/','IBM':'https://www.ibm.com/careers','Amazon':'https://www.amazon.jobs/','Microsoft':'https://careers.microsoft.com/','EY':'https://www.ey.com/en_in/careers'}

CONTENT = {
'percentage':('Percentage measures a quantity relative to 100.','Base value, percentage change, successive percentage change.','Percentage = part/whole × 100; new value = original × (1 ± p/100).','For successive changes use net change = a+b+ab/100 with signs.','If 25% of x is 60, x = 240.','Focus on translating word problems into base and change.'),
'profit-loss':('Profit and loss compares selling price with cost price.','CP, SP, profit, loss, discount, marked price.','Profit%=(SP-CP)/CP×100; Loss%=(CP-SP)/CP×100.','Use CP as the base for profit/loss percentage.','CP ₹500 and SP ₹600 gives 20% profit.','Track whether the percentage is based on CP or MP.'),
'simple-interest':('Simple interest grows linearly on the principal.','Principal, rate, time, amount.','SI=P×R×T/100; Amount=P+SI.','Convert months into years before applying the formula.','P=2000,R=5%,T=2 gives SI=200.','Check units before calculating.'),
'compound-interest':('Compound interest adds interest to the running amount.','Annual/half-yearly compounding, amount, growth factor.','A=P(1+r/100)^n; CI=A-P.','For half-yearly compounding halve the rate and double periods.','1000 at 10% for 2 years gives 1210.','Use the growth-factor approach for speed.'),
'ratio-proportion':('Ratios compare quantities in the same units.','Equivalent ratios, proportions, direct/inverse variation.','a:b = ka:kb; a/b=c/d ⇒ ad=bc.','Normalize units before forming ratios.','2:3 scaled by 4 becomes 8:12.','Look for a common multiplier first.'),
'averages':('Average is the arithmetic mean of observations.','Total, count, weighted average.','Average=total/count.','When one value changes, adjust the total rather than recomputing all values.','Average of 10,20,30 is 20.','Convert averages into totals whenever possible.'),
'time-work':('Work-rate problems relate completed work to time.','Rates, combined work, efficiency.','If A takes x days, rate=1/x; combined rate is the sum.','Use LCM to avoid fractions when solving quickly.','A in 10 days completes 1/10 per day.','Never add days directly; add rates.'),
'pipes-cisterns':('Pipes use the same work-rate principle with filling and emptying rates.','Inlet, outlet, net rate.','Net rate = filling rates - emptying rates.','Take tank capacity as 1 unit.','A fills in 6h and B empties in 12h: net rate=1/12.','Treat leaks as negative work.'),
'time-speed-distance':('Motion problems connect distance, speed and time.','Relative speed, average speed, unit conversion.','D=S×T; S=D/T; T=D/S.','Convert km/h to m/s by ×5/18.','60 km/h for 2h covers 120 km.','For average speed, use total distance/total time.'),
'trains':('Train questions combine speed with the length covered while crossing an object.','Train length, platform length, relative speed.','Time = distance/speed.','Convert km/h to m/s before using metres.','A 100m train at 10m/s crosses a pole in 10s.','For platform crossing, distance is train+platform length.'),
'boats-streams':('Boat problems use still-water speed and stream speed.','Upstream/downstream, still-water speed.','Downstream=b+s; upstream=b-s.','Boat speed=(downstream+upstream)/2.','Downstream 12 and upstream 8 gives boat speed 10.','Keep directions explicit.'),
'mixtures-alligation':('Mixture problems combine quantities at different rates or prices.','Weighted average, alligation.','Mean price = total value/total quantity.','Use cross-difference for ratio when two rates are mixed.','₹20 and ₹30 mixed to get ₹24: ratio 3:2.','Check that the target lies between component values.'),
'partnership':('Partnership shares depend on capital and time.','Capital, time, profit ratio.','Share ∝ capital×time.','Convert all time periods to the same unit.','₹10k for 12m and ₹20k for 6m are equal profit units.','Multiply capital by duration.'),
'number-system':('Number system covers divisibility, remainders, primes and place values.','Factors, multiples, divisibility, remainders.','Use divisibility rules and modular arithmetic.','For last-digit questions, inspect cycles.','A number divisible by 2 ends in an even digit.','Reduce large arithmetic with modular patterns.'),
'hcf-lcm':('HCF is the greatest common factor; LCM is the least common multiple.','Prime factorization, Euclidean algorithm.','For two positive integers, HCF×LCM=product.','Factorize only as much as needed.','HCF of 12 and 18 is 6.','Use Euclid for large numbers.'),
'probability':('Probability measures the chance of an event.','Sample space, favorable outcomes, complement.','P(E)=favorable/total for equally likely outcomes.','Use complement for “at least one” problems.','Probability of a head on a fair coin is 1/2.','Keep numerator and denominator from the same sample space.'),
'permutation-combination':('Permutations arrange; combinations select.','Factorials, nPr, nCr.','nPr=n!/(n-r)!; nCr=n!/[r!(n-r)!].','Ask whether order matters before choosing the formula.','Choosing 2 from 5 gives 10 combinations.','Exploit symmetry nCr=nC(n-r).'),
'ages':('Age problems translate verbal relationships into equations.','Present age, past/future age, ratios.','Age changes by the same number of years for everyone.','Set the present age as a variable and shift by ± years.','If A is 5 years older than B, A-B=5 always.','Use ratio information at the stated time.'),
'clocks':('Clock problems use relative angular motion of hands.','Angles, coincidence, right angles.','Minute hand moves 6°/min; hour hand 0.5°/min.','Relative speed is 5.5°/min.','At 3:00 the angle is 90°.','For exact times use angle equations.'),
'calendars':('Calendar problems use odd days and leap-year rules.','Leap years, day shifts, day-of-week.','Ordinary year=1 odd day; leap year=2.','Century years are leap only if divisible by 400.','2000 is leap; 1900 is not.','Track cumulative odd days modulo 7.'),
'data-interpretation':('DI converts tables and charts into quantitative comparisons.','Ratios, percentages, totals, averages.','Read values first, then compute only what is asked.','Estimate before calculating to catch option traps.','A bar of 40 versus 50 means 25% increase from 40.','Watch units and chart scales.'),
'simplification':('Simplification combines arithmetic operations efficiently.','BODMAS, fractions, decimals, surds.','Order: brackets, orders, division, multiplication, addition, subtraction.','Cancel factors before multiplying.','(20+10)×2=60.','Do exact arithmetic before rounding.'),
'algebra':('Algebra represents unknown quantities with variables and equations.','Linear equations, identities, factorization.','Solve by maintaining equality on both sides.','Factor common terms before expanding.','2x+6=14 gives x=4.','Translate words into equations first.'),
'geometry':('Geometry studies properties of shapes, lines and angles.','Triangles, quadrilaterals, circles, angles.','Triangle angle sum=180°; Pythagoras a²+b²=c².','Draw a quick diagram when possible.','A 3-4-5 triangle is right-angled.','Use known angle and side relationships.'),
'mensuration':('Mensuration calculates perimeter, area and volume.','2D area, perimeter, 3D surface area and volume.','Rectangle area=l×b; circle area=πr²; cuboid volume=lbh.','Keep square/cubic units consistent.','5×4 rectangle area is 20 square units.','Write the formula before substituting values.')}

REASON_INTRO = {
'analogy':('Analogy identifies a consistent relationship between two pairs.','Word, number and functional relationships.','Find the exact relationship before selecting the option.','Check whether the relation is function, category, part-whole or degree.','Book:Reading :: Fork:Eating.','Avoid choosing an option based only on superficial similarity.'),
'number-series':('Number series asks you to discover a mathematical pattern.','Differences, ratios, alternating operations.','Compare first differences and ratios.','Check alternating terms when a simple pattern fails.','2,4,8,16 → multiply by 2.','Test the simplest consistent rule first.'),
'alphabet-series':('Alphabet series follows position-based letter patterns.','Forward/backward shifts, alternating patterns.','A=1,…,Z=26.','Convert letters to positions to spot numeric patterns.','A,C,E,G follows +2 positions.','Watch wrap-around after Z.'),
'coding-decoding':('Coding-decoding transforms letters or words using a stated or hidden rule.','Shifts, reversals, substitutions, positions.','Map symbols consistently and verify on every given example.','Use A1Z26 positions for shift-based codes.','CAT shifted +1 becomes DBU.','Never infer a rule from one character alone.'),
'blood-relations':('Blood relation questions test family relationships.','Parent, sibling, child, spouse, generation.','Represent relationships as a small family tree.','Resolve pronouns before calculating the final relation.','Mother’s brother is maternal uncle.','Draw instead of holding the whole chain in memory.'),
'direction-sense':('Direction problems track movement and final position.','North, south, east, west, distance.','Use coordinates: east +x, north +y.','Cancel opposite movements before calculating distance.','3 km north then 3 km south returns to origin.','Separate final direction from total distance.'),
'syllogisms':('Syllogisms test whether conclusions follow from stated premises.','All, some, no, possibility.','Use set relationships and valid inference rules.','Do not assume information not stated.','All A are B does not mean all B are A.','Check necessity, not plausibility.'),
'statements-conclusions':('Conclusions must logically follow from the statement.','Scope, certainty, implication.','Use only information contained in the statement.','Reject conclusions that add outside assumptions.','“All roses are flowers” supports “Some flowers are roses” only if existence is given; be precise.','Distinguish implication from possibility.'),
'statements-assumptions':('Assumptions are unstated ideas required for a statement to make sense.','Necessary assumptions, context.','Ask what must be true for the statement to hold.','Avoid assumptions that merely could be true.','A recommendation usually assumes the recommended action is feasible.','Test necessity by negating the assumption.'),
'seating-arrangement':('Seating arrangement problems place people under positional constraints.','Linear/circular seating, adjacency, opposite positions.','Anchor one person first in circular arrangements.','Translate every clue into a positional constraint.','If A sits left of B, preserve that order.','Use a small table/grid.'),
'puzzles':('Logic puzzles combine multiple constraints into a consistent arrangement.','Ordering, matching, grouping, scheduling.','Create a grid and eliminate impossible combinations.','Apply the strongest constraints first.','A fixed day or position is a useful anchor.','Do not guess when elimination can solve it.'),
'ranking-order':('Ranking questions determine relative positions.','Rank from top/bottom, swaps, counts between people.','If rank from top is r and total is n, bottom rank=n-r+1.','Keep the reference direction explicit.','3rd from top in 10 is 8th from bottom.','Use formulas for quick conversions.'),
'venn-diagrams':('Venn diagrams represent set relationships and overlaps.','Union, intersection, complements.','For two sets: n(A∪B)=n(A)+n(B)-n(A∩B).','Draw circles before calculating.','10+8-3=15 in the union.','Avoid double-counting overlap.'),
'classification':('Classification identifies the item that does not share the common property.','Category, function, numeric or structural property.','State the common property explicitly.','Choose the strongest shared rule.','Three programming languages and one database may form a category distinction.','Do not rely on spelling alone.'),
'odd-one-out':('Odd-one-out questions ask for the unique member of a set.','Patterns in numbers, words, shapes and concepts.','Compare all items against the same property.','Check category and structural differences.','2,4,6,9: 9 is odd while the others are even.','Prefer objective properties.'),
'data-sufficiency':('Data sufficiency asks whether statements provide enough information to answer a question.','Statement combinations, yes/no sufficiency.','Test each statement independently, then together.','You need enough information, not the exact value necessarily.','A single equation with one unknown is sufficient.','Avoid solving more than required.'),
'logical-reasoning':('Logical reasoning evaluates arguments, patterns and conditions.','Inference, cause-effect, assumptions, constraints.','Separate facts from conclusions.','Use formal conditions when available.','If A implies B and A is true, B follows.','Do not reverse implications.'),
'non-verbal-reasoning':('Non-verbal reasoning identifies visual patterns and transformations.','Rotation, reflection, counting, sequence.','Track one transformation at a time.','Compare orientation, count and relative position.','A 90° rotation changes orientation but preserves shape.','Mentally isolate invariant features.'),
'reasoning-clocks':('Clock reasoning applies angular relationships to logic questions.','Hand positions, angle changes.','Minute hand 6°/minute; hour hand 0.5°/minute.','Use relative angular speed.','At 6:00 the hands are 180° apart.','Use a timeline for interval questions.'),
'reasoning-calendars':('Calendar reasoning uses recurring seven-day cycles.','Odd days, leap years, day offsets.','Reduce day shifts modulo 7.','Apply leap-year rules carefully.','A 7-day shift leaves the weekday unchanged.','Check the year boundary.'),
}

def add_question(topic, text, options, answer, explanation, difficulty='Medium'):
    existing=Question.query.filter_by(topic_id=topic.id,question=text).first()
    if existing:return existing
    q=Question(question=text,correct_answer=answer,explanation=explanation,topic=topic,category=topic.category,difficulty=difficulty,tags=topic.slug)
    db.session.add(q); db.session.flush()
    for i,o in enumerate(options):db.session.add(QuestionOption(question=q,label=chr(65+i),text=str(o)))
    return q

def aptitude_question(slug,i):
    n=i+1
    if slug=='percentage':
        base=80+n*10; p=10+(n%6)*5; val=base*p//100
        return f'What is {p}% of {base}?',[str(val),str(val+10),str(val-5),str(val+20)],'A',f'{p}/100 × {base} = {val}.'
    if slug=='profit-loss':
        cp=100+n*25; pct=10+(n%5)*5; sp=cp*(100+pct)//100
        return f'An item costs ₹{cp}. If it is sold at a profit of {pct}%, what is the selling price?',[str(sp),str(sp+cp//10),str(cp),str(sp-10)],'A',f'SP = CP × (1 + {pct}/100) = ₹{sp}.'
    if slug=='simple-interest':
        p=1000+n*100;r=5+(n%4);t=1+(n%3);si=p*r*t//100
        return f'Find the simple interest on ₹{p} at {r}% per annum for {t} year(s).',[str(si),str(si+100),str(si-50),str(p+si)],'A',f'SI=P×R×T/100 = {si}.'
    if slug=='compound-interest':
        p=1000+n*100;r=10;t=2;amount=p*(1+r/100)**t;ans=round(amount)
        return f'What is the amount on ₹{p} at {r}% compound interest annually for {t} years?',[str(ans),str(ans-100),str(ans+100),str(p+200)],'A',f'A=P(1+r/100)^n = ₹{ans}.'
    if slug=='ratio-proportion':
        a=2+n;b=3+(n%7);k=2+(n%5)
        return f'If a:b = {a}:{b}, what is a when b = {b*k}?',[str(a*k),str(b*k),str(a+b),str(k)],'A',f'Scale both terms by {k}; a={a*k}.'
    if slug=='averages':
        a=10+n;b=20+n;c=30+n;avg=(a+b+c)//3
        return f'What is the average of {a}, {b} and {c}?',[str(avg),str(avg+1),str(avg-1),str(a+b+c)],'A',f'Sum={a+b+c}; average={avg}.'
    if slug in ('time-work','pipes-cisterns'):
        a=5+(n%12);b=11+n;den=a*b//__import__('math').gcd(a,b);days=den//(a+b) if den%(a+b)==0 else round(1/(1/a+1/b),2)
        ans=str(days)
        return f'A worker can finish a job in {a} days and another in {b} days. What is their combined time?',[ans,str(round(float(days)+1,2)),str(a+b),str(abs(a-b))],'A',f'Combined rate = 1/{a}+1/{b}; time is the reciprocal.'
    if slug in ('time-speed-distance','trains'):
        speed=30+(n%10)*5;time=2+(n%7);dist=speed*time
        return f'A vehicle travels at {speed} km/h for {time} hours. What distance does it cover?',[f'{dist} km',f'{dist+10} km',f'{dist-10} km',f'{speed+time} km'],'A',f'Distance = speed × time = {dist} km.'
    if slug=='boats-streams':
        down=12+(n%10)*2;up=6+(n%8);boat=(down+up)//2
        return f'A boat moves downstream at {down} km/h and upstream at {up} km/h. Find its still-water speed.',[str(boat),str(down-up),str(down+up),str(up)],'A',f'Still-water speed = ({down}+{up})/2 = {boat} km/h.'
    if slug=='mixtures-alligation':
        x=20+n;y=x+10;target=x+4+(n%3);ratio=(y-target)//(target-x)
        return f'₹{x} and ₹{y} items are mixed to obtain ₹{target} average price. What is the ratio of cheaper to costlier items?',[f'{ratio}:1','1:1',f'1:{ratio}',f'{ratio+1}:1'],'A',f'By alligation, cheaper:costlier = ({y}-{target}):({target}-{x}) = {ratio}:1.'
    if slug=='partnership':
        c1=10000+n*500;c2=20000+n*300;t1=12;t2=6;u1=c1*t1;u2=c2*t2
        from math import gcd
        g=gcd(u1,u2);return (f'Partners invest ₹{c1} for {t1} months and ₹{c2} for {t2} months. What is their profit ratio?', [f'{u1//g}:{u2//g}', str(u1//g)+':'+str(u2//g), str(c1//c2)+':1', '1:1'], 'A', f'Profit ratio follows capital×time: {u1}:{u2}.')
    if slug=='number-system':
        x=100+n*7;rem=x%9
        return f'What is the remainder when {x} is divided by 9?',[str(rem),str((rem+1)%9),str((rem+2)%9),str(9-rem if rem else 0)],'A',f'{x} = 9q + {rem}, so the remainder is {rem}.'
    if slug=='hcf-lcm':
        a=12+n%8;b=18+n%7
        import math
        h=math.gcd(a,b);return f'Find the HCF of {a} and {b}.',[str(h),str(a+b),str(abs(a-b)),str(a*b)],'A',f'The greatest common divisor of {a} and {b} is {h}.'
    if slug=='probability':
        fav=2+(n%4);total=6+(n%5)
        from fractions import Fraction
        f=Fraction(fav,total)
        return f'A fair experiment has {total} equally likely outcomes, of which {fav} are favourable. What is the probability?',[str(f),str(Fraction(fav+1,total)),str(Fraction(1,total)),str(Fraction(total-fav,total))],'A',f'Probability = favourable/total = {f}.'
    if slug=='permutation-combination':
        from math import comb
        nn=5+(n%26);r=2;ans=comb(nn,r)
        return f'How many ways can {r} people be selected from {nn} people?',[str(ans),str(nn*2),str(nn**2),str(nn+r)],'A',f'Use nCr: C({nn},{r})={ans}.'
    if slug=='ages':
        b=20+n;a=b+5;future=3
        return f'A is 5 years older than B. If B is {b} now, what will A be after {future} years?',[str(a+future),str(b+future),str(a),str(b+5+future+1)],'A',f'A is {a} now, so after {future} years A will be {a+future}.'
    if slug=='clocks':
        h=1+(n%12);ang=min(30*h,360-30*h)
        return f'What is the smaller angle between the hands at {h}:00?',[f'{ang}°',f'{360-ang}°','90°','180°'],'A',f'At {h}:00 the minute hand is at 12 and hour hand at {h}×30°.'
    if slug in ('calendars','reasoning-calendars'):
        y=2000+n
        leap=(y%400==0) or (y%4==0 and y%100!=0)
        return f'Is the year {y} a leap year?',['Yes','No','Only if January is Monday','Cannot determine'],'A' if leap else 'B',f'{y} is a leap year.' if leap else f'{y} is not a leap year.'
    if slug=='data-interpretation':
        a=40+n;b=50+n;inc=round((b-a)/a*100,2)
        return f'A value rises from {a} to {b}. What is the percentage increase?',[f'{inc}%','10%','20%',f'{inc+5}%'],'A',f'Increase = ({b}-{a})/{a}×100 = {inc}%.'
    if slug=='simplification':
        a=10+n;b=2+(n%5);ans=(a+b)*2
        return f'Simplify ({a}+{b})×2.',[str(ans),str(a+b),str(ans+2),str(a*b)],'A',f'First add: {a+b}; then multiply by 2 = {ans}.'
    if slug=='algebra':
        x=3+n;b=2*(x+1);ans=x
        return f'Solve 2x + {b-2*x} = {b}.',[str(ans),str(ans+1),str(ans-1),str(b)],'A',f'2x={b-(b-2*x)}={2*x}, so x={ans}.'
    if slug=='geometry':
        a=3+n%12;b=4+n%11;c=(a*a+b*b)**0.5
        if abs(c-round(c))<1e-9: val=int(round(c))
        else: val=round(c,2)
        return f'A right triangle has legs {a} and {b}. What is the hypotenuse approximately?',[str(val),str(a+b),str(abs(a-b)),str(a*b)],'A',f'By Pythagoras, c=√({a}²+{b}²)≈{val}.'
    if slug=='mensuration':
        l=4+n%7;b=3+n%5;area=l*b
        return f'What is the area of a rectangle with length {l} and breadth {b}?',[str(area),str(2*(l+b)),str(l+b),str(l*b+1)],'A',f'Area = length×breadth = {area}.'
    return f'Which statement is directly associated with {slug.replace("-"," ")}?',[slug.replace('-',' ').title(),'Unrelated concept','None','All of these'],'A',f'This question is scoped specifically to {slug.replace("-"," ")}.', 'Easy'

def reasoning_question(slug,i):
    n=i+1
    if slug=='number-series':
        start=2+n;ans=start*2**3
        return f'Find the next term: {start}, {start*2}, {start*4}, {start*8}, ?',[str(ans),str(ans-2),str(ans+2),str(start*9)],'A','Each term is multiplied by 2.'
    if slug=='alphabet-series':
        pos=1+(n%8);letters=[chr(64+pos+2*k) for k in range(4) if pos+2*k<=26];nextp=pos+8
        if nextp>26:nextp=((nextp-1)%26)+1
        ans=chr(64+nextp);return f'Find the next letter: {", ".join(letters)}, ?',[ans,chr(64+(nextp%26)+1),chr(64+((nextp-2-1)%26)+1),'Z'],'A','The letters advance by two positions.'
    if slug=='coding-decoding':
        shift=1+(n%4);base=chr(65+(n%20));word=base+chr(65+((n*3)%26))+chr(65+((n*5)%26));coded=''.join(chr((ord(c)-65+shift)%26+65) for c in word)
        return f'If each letter of {word} is shifted {shift} position(s) forward, how is it coded?',[coded,word[::-1],''.join(chr((ord(c)-65+shift+1)%26+65) for c in word),word],'A',f'Each letter moves {shift} position(s) forward.'
    if slug=='analogy':
        a=2+n;b=a*2;c=a+1;ans=c*2
        return f'{a} is to {b} as {c} is to:',[str(ans),str(c+1),str(c*3),str(a+b)],'A',f'The relationship is multiplication by 2: {c}×2={ans}.'
    if slug=='blood-relations':
        names=[('Ravi','Priya','Kiran'),('Arun','Meena','Dev'),('Vikram','Anita','Riya'),('Karan','Sita','Neel'),('Aman','Pooja','Raj'),('Nikhil','Sara','Ishaan')];a,b,c=names[n%len(names)]
        return f'If {a} is the brother of {b} and {b} is the mother of {c}, how is {a} related to {c}?',['Uncle','Father','Brother','Cousin'],'A','Mother’s brother is the child’s maternal uncle.'
    if slug=='direction-sense':
        d=3+n%10;return f'A person walks {d} km north and then {d} km south. Where are they relative to the starting point?',['At the starting point',f'{d} km north',f'{d} km south','Cannot determine'],'A','Equal opposite movements cancel.'
    if slug=='syllogisms':
        labels=['engineers','designers','analysts','developers','graduates','managers'];a=labels[n%len(labels)];b='professionals';c='learners'
        return f'Statements: All {a} are {b}. All {b} are {c}. Which conclusion is definitely valid?',[f'All {a} are {c}',f'All {c} are {a}',f'No {a} are {c}',f'Some {c} are not {b}'],'A',f'If all {a} are {b} and all {b} are {c}, then all {a} are {c}.'
    if slug=='statements-conclusions':
        subjects=['registered candidates','library members','exam applicants','internship trainees','club participants','scholarship applicants'];sub=subjects[n%len(subjects)]
        return f'Statement: All {sub} must follow the published guidelines. Which conclusion follows?',[f'Every {sub[:-1] if sub.endswith("s") else sub} must follow the published guidelines','Every person follows the guidelines','Only candidates have guidelines','No one needs guidelines'],'A','The conclusion directly follows from the universal statement.'
    if slug=='statements-assumptions':
        prompts=['Use this course to improve your SQL skills.','Join the practice test to improve speed.','Attend the workshop to learn cloud basics.','Use the mock interview to improve communication.','Read the guide to improve DSA fundamentals.','Practice daily to improve accuracy.'];prompt=prompts[n%len(prompts)]
        return f'Statement: “{prompt}” Which assumption is necessary?',[f'The learner has a reason to improve the stated skill','Everyone already knows the skill','The activity is free','The skill is unrelated to the goal'],'A','The recommendation assumes that improving the stated skill is relevant to the learner.'
    if slug in ('seating-arrangement','puzzles'):
        people=[('A','B','C'),('P','Q','R'),('L','M','N'),('X','Y','Z'),('D','E','F'),('G','H','I'),('J','K','L'),('M','N','O')];a,b,c=people[n%len(people)]
        return f'{a}, {b} and {c} sit in a row. {a} sits left of {b} and {c} sits right of {b}. Who is in the middle?',[b,a,c,'Cannot determine'],'A',f'The order is {a}-{b}-{c}, so {b} is in the middle.'
    if slug=='ranking-order':
        total=10+n%18;top=2+n%6;bottom=total-top+1
        return f'A student is {top}th from the top in a class of {total}. What is the rank from the bottom?',[str(bottom),str(top),str(total-top),str(total+top)],'A','Bottom rank = total - top rank + 1.'
    if slug=='venn-diagrams':
        a=20+n;b=15+n;inter=5+n%7;union=a+b-inter
        return f'If set A has {a} members, set B has {b}, and their intersection has {inter}, how many are in A∪B?',[str(union),str(a+b),str(inter),str(a+b+inter)],'A','Union = A + B - intersection.'
    if slug in ('classification','odd-one-out'):
        nums=[2+n*2,4+n*2,6+n*2,9+n*2]
        return f'Which number is different: {nums[0]}, {nums[1]}, {nums[2]}, {nums[3]}?',[str(nums[3]),str(nums[0]),str(nums[1]),str(nums[2])],'A','The first three are even; the last is odd.'
    if slug=='data-sufficiency':
        vals=[5,7,9,11,13,15];v=vals[n%len(vals)]
        return f'Question: Is x > 0? Statement I: x={v}. Statement II: x²={v*v}. Which is sufficient?',['I alone','II alone','Both together','Neither'],'A','Statement I directly establishes x>0.'
    if slug=='logical-reasoning':
        a=f'A{n}';b=f'B{n}';c=f'C{n}'
        return f'If all {a} are {b} and all {b} are {c}, which statement must be true?',[f'All {a} are {c}',f'All {c} are {a}',f'Some {c} are not {b}',f'No {a} are {c}'],'A','Transitivity gives A ⊆ B ⊆ C.'
    if slug=='non-verbal-reasoning':
        deg=45+(n%7)*45
        return f'A shape is rotated by {deg}°. Which property remains unchanged?',['Number of sides','Orientation','Position','Direction'],'A','Rotation changes orientation/position but preserves the number of sides.'
    if slug in ('clocks','reasoning-clocks'):
        h=1+(n%12);ang=min(h*30,360-h*30)
        return f'What is the smaller angle between the hands at {h}:00?',[f'{ang}°',f'{180-ang}°','90°','0°'],'A',f'At {h}:00 the smaller hand separation is {ang}°.'
    if slug in ('calendars','reasoning-calendars'):
        y=2001+n;leap=(y%400==0) or (y%4==0 and y%100!=0)
        return f'Is the year {y} a leap year?',['Yes','No','Only if January is Monday','Cannot determine'],'A' if leap else 'B',f'{y} is a leap year.' if leap else f'{y} is not a leap year.'
    return f'Which option best represents the core idea of {slug.replace("-"," ")} #{n}?',[slug.replace('-',' ').title(),f'Unrelated concept {n}','Random choice','None'],'A',f'The question is specifically scoped to {slug.replace("-"," ")}.','Easy'

def seed_topics():
    qa=db.session.query(Category).filter_by(kind='aptitude').first() or Category(name='Quantitative Aptitude',kind='aptitude');db.session.add(qa) if qa.id is None else None
    qr=db.session.query(Category).filter_by(kind='reasoning').first() or Category(name='Logical Reasoning',kind='reasoning');db.session.add(qr) if qr.id is None else None
    db.session.flush()
    for name,slug in APT_TOPICS:
        t=Topic.query.filter_by(slug=slug).first()
        if not t:t=Topic(name=name,slug=slug,category=qa);db.session.add(t);db.session.flush()
        if not t.description:t.description=f'{name}: concepts, formulas, shortcuts, solved examples and placement practice.'
        if not t.content:
            intro,concept,formula,shortcut,example,note=CONTENT.get(slug,(f'Learn {name} step by step.','Core concepts and common placement patterns.','Use the standard rules for this topic.','Start with the simplest representation.','Practice a worked example before timed questions.','Focus on accuracy first, then speed.'))
            db.session.add(TopicContent(topic=t,introduction=intro,concepts=concept,formulas=formula,shortcuts=shortcut,examples=example,placement_notes=note,faq=f'What is {name}? Study the concepts, examples and then take the topic mock test.'))
        for i in range(30):
            text,opts,ans,exp=aptitude_question(slug,i); text=f'{text} (Practice Set {i+1})'; add_question(t,text,opts,ans,exp,'Easy' if i<10 else ('Medium' if i<24 else 'Hard'))
    for name,slug in REASON_TOPICS:
        t=Topic.query.filter_by(slug=slug).first()
        if not t:t=Topic(name=name,slug=slug,category=qr);db.session.add(t);db.session.flush()
        if not t.description:t.description=f'{name}: logical concepts, examples, shortcuts and placement practice.'
        if not t.content:
            intro,concept,formula,shortcut,example,note=REASON_INTRO.get(slug,(f'Learn {name} using structured reasoning.','Core patterns and inference rules.','Use the stated constraints and logical relationships.','Translate clues into a small diagram or table.','Work through a simple example before timing yourself.','Avoid assumptions not supported by the question.'))
            db.session.add(TopicContent(topic=t,introduction=intro,concepts=concept,formulas=formula,shortcuts=shortcut,examples=example,placement_notes=note,faq=f'How do I prepare for {name}? Learn the pattern, solve examples, then take the topic mock test.'))
        for i in range(30):
            text,opts,ans,exp=reasoning_question(slug,i); text=f'{text} (Practice Set {i+1})'; add_question(t,text,opts,ans,exp,'Easy' if i<10 else ('Medium' if i<24 else 'Hard'))
    db.session.commit()

def seed_companies():
    for name,url in COMPANIES.items():
        c=Company.query.filter_by(name=name).first()
        if not c:
            c=Company(name=name,overview=f'{name} preparation hub.',eligibility='Check the latest official recruitment notice for role, batch and eligibility.',pattern='Assessment structure can change; verify current details before applying.',stages='May include assessment, technical and HR stages depending on role.');db.session.add(c);db.session.flush()
        if not RecruitmentLink.query.filter_by(company_id=c.id).first():db.session.add(RecruitmentLink(company=c,url=url))
        for topic in ['Quantitative Aptitude','Logical Reasoning','Verbal Ability','Coding']:
            a=CompanyAssessment.query.filter_by(company_id=c.id,topic=topic).first()
            if not a:
                a=CompanyAssessment(company=c,title=f'{name} {topic} Assessment',topic=topic,duration_minutes=60,description=f'Practice {topic} for {name}. Verify current official pattern before using it as a representation of a live hiring test.');db.session.add(a);db.session.flush()
            if not CompanyAssessmentQuestion.query.filter_by(assessment_id=a.id).first():
                kind='aptitude' if topic=='Quantitative Aptitude' else ('reasoning' if topic=='Logical Reasoning' else None)
                qs=Question.query.join(Category).filter(Category.kind==kind).order_by(Question.id).limit(30).all() if kind else []
                for pos,q in enumerate(qs,1):db.session.add(CompanyAssessmentQuestion(assessment=a,question=q,position=pos))
        if not ModelPaper.query.filter_by(company_id=c.id).first():db.session.add(ModelPaper(company=c,title=f'{name} Model Paper 1',status='Coming Soon'))
    db.session.commit()

def seed_tests():
    # Topic tests: exactly 30 questions, scoped to one topic.
    for t in Topic.query.filter(Topic.slug.in_([s for _,s in APT_TOPICS+REASON_TOPICS])).all():
        title=f'{t.name} Mock Test'
        test=Test.query.filter_by(title=title).first()
        if not test:
            test=Test(title=title,category=t.category.name,topic=t,difficulty='Medium',duration_minutes=20,published=True,instructions=f'30 {t.name} questions. This test is strictly scoped to the selected topic.');db.session.add(test);db.session.flush()
        if len(test.questions)<30:
            existing={x.question_id for x in test.questions}
            qs=Question.query.filter_by(topic_id=t.id,active=True).order_by(Question.id).all()
            for pos,q in enumerate(qs[:30],1):
                if q.id not in existing:db.session.add(TestQuestion(test=test,question=q,position=pos))
    # General categories without mixing topic tests.
    db.session.commit()

def seed_coding():
    langs=[('C','c','terminal'),('C++','cpp','code-2'),('Java','java','coffee'),('Python','python','braces'),('JavaScript','javascript','file-code-2'),('SQL','sql','database')]
    for name,slug,icon in langs:
        if not CodingLanguage.query.filter_by(slug=slug).first():db.session.add(CodingLanguage(name=name,slug=slug,icon=icon))
    db.session.commit()
    py=CodingLanguage.query.filter_by(slug='python').first()
    if not CodingProblem.query.filter_by(title='Two Sum',language_id=py.id).first():
        cp=CodingProblem(title='Two Sum',difficulty='Easy',description='Given an array of integers and a target, return the indices of two numbers that add up to the target.',starter_code='def two_sum(nums, target):\n    # write your solution\n    pass',tags='arrays,hashing',language=py,input_format='nums: list[int], target: int',output_format='two indices',constraints='2 <= len(nums) <= 10^5',examples='Input: [2,7,11,15], 9\nOutput: [0,1]');db.session.add(cp);db.session.flush();db.session.add(CodingTestCase(problem=cp,input='[2,7,11,15], 9',expected_output='[0,1]',hidden=False));db.session.add(CodingTestCase(problem=cp,input='[3,2,4], 6',expected_output='[1,2]',hidden=True))
    db.session.commit()

def seed_dsa():
    cats=['Arrays','Strings','Hashing','Searching','Sorting','Linked Lists','Stack','Queue','Recursion','Binary Trees','BST','Heaps','Graphs','Greedy','Dynamic Programming','Two Pointers','Sliding Window','Backtracking']
    existing=DSAProblem.query.count()
    if existing>=75:return
    for i in range(existing+1,76):
        cat=cats[(i-1)%len(cats)];diff='Easy' if i<=25 else ('Medium' if i<=60 else 'Hard')
        db.session.add(DSAProblem(title=f'Placement DSA Problem {i}: {cat} Pattern', category=cat, difficulty=diff, statement=f'Solve a placement-oriented {cat.lower()} problem #{i}. Define the required input, produce the expected output, and handle the stated edge cases.', examples='Example input/output should be used to validate the pattern.', explanation=f'Identify the {cat.lower()} pattern, choose the data structure or technique, and validate edge cases.', approach=f'Use a standard {cat.lower()} approach, explain why it works, and avoid unnecessary passes.', complexity='Target O(n) or the best practical complexity for the pattern.', tags=cat.lower().replace(' ','-')))
    db.session.commit()

def seed_interviews():
    hr=[('Tell me about yourself.','Communication, structure and relevance.','Use Present → Past → Future. Keep it role-focused.','I am a final-year engineering student with a strong interest in software and placement-oriented problem solving. I have built projects, practiced technical fundamentals and enjoy learning by solving real problems. I am now looking for an entry-level role where I can contribute and grow.','Tell me about one project you are proud of.'),('What are your strengths?','Self-awareness and evidence.','Name two strengths and support each with a short example.','One strength is structured problem solving. I break a large task into smaller steps and validate each step. Another is consistency: I maintain a regular practice routine and track progress.','Can you give a recent example?'),('What is a weakness you are working on?','Honesty and improvement mindset.','Choose a real but manageable weakness and explain the improvement plan.','Earlier I sometimes spent too long polishing one part of a task. I now time-box work, prioritize the highest-impact items and review at the end.','How has that changed your work?'),('Why should we hire you?','Role fit and evidence, not memorized claims.','Connect skills, projects and learning attitude to the role.','I bring a combination of fundamentals, practical project experience and a strong willingness to learn. I focus on understanding requirements, communicating clearly and improving through feedback.','Which skill would you contribute first?'),('Why do you want to join our company?','Preparation and motivation.','Mention the company’s role, learning opportunity and relevant work after researching the current official information.','I am interested because the role aligns with the skills I have been developing and gives me an opportunity to work on real problems while learning from experienced teams. I would tailor this answer to the specific role and company.','What do you know about our current work?')]
    tech=[('Python','Explain list vs tuple in Python.'),('Python','What is a Python dictionary and when would you use it?'),('Java','Explain method overloading and overriding.'),('Java','What is the difference between JDK, JRE and JVM?'),('C','Explain pointers and their common use cases.'),('C++','What is the difference between stack and heap memory?'),('JavaScript','Explain var, let and const.'),('SQL','What is the difference between WHERE and HAVING?'),('SQL','Explain INNER JOIN and LEFT JOIN.'),('DBMS','What is normalization and why is it used?'),('DBMS','Explain ACID properties.'),('Data Structures','When would you use a stack instead of a queue?'),('Data Structures','What is the average lookup complexity of a hash table?'),('DSA','Explain binary search and its complexity.'),('DSA','What is the difference between BFS and DFS?'),('OS','What is a process and how is it different from a thread?'),('OS','What is deadlock and what are its necessary conditions?'),('CN','What is the difference between TCP and UDP?'),('OOP','Explain encapsulation, inheritance, polymorphism and abstraction.'),('Cloud','What is virtualization in cloud computing?')]
    if InterviewQuestion.query.count() < 25:
        for q,check,how,ans,follow in hr:
            db.session.add(InterviewQuestion(category='HR',topic='HR',question=q,interviewer_checking=check,how_to_answer=how,sample_answer=ans,follow_up=follow))
        for topic,q in tech:
            db.session.add(InterviewQuestion(category='Technical',topic=topic,question=q,interviewer_checking='Conceptual clarity, correctness and ability to apply the idea.',how_to_answer='Define it, explain the mechanism, give a practical example and mention an important trade-off.',sample_answer=f'A strong answer should define {q.rstrip("?")} clearly, explain why it matters and give a small example. Avoid memorized one-line definitions.',follow_up='Can you explain this with a practical example?'))
        db.session.commit()

def seed_achievements():
    vals=[('First Mock','Complete your first mock test',20),('100 Questions','Solve 100 practice questions',50),('7-Day Streak','Practice for seven consecutive days',100),('90% Accuracy','Reach 90% accuracy',150),('DSA Starter','Complete your first DSA problem',40)]
    for n,d,x in vals:
        if not Achievement.query.filter_by(name=n).first():db.session.add(Achievement(name=n,description=d,xp=x))
    db.session.commit()

def seed_database():
    # Always make the database progressively richer; never stop just because a user exists.
    if not User.query.filter_by(email='admin@placeprep.local').first():
        admin=User(name='PlacePrep Admin',email='admin@placeprep.local',role='admin');admin.set_password('Admin@123');db.session.add(admin)
    if not User.query.filter_by(email='student@placeprep.local').first():
        student=User(name='Demo Student',email='student@placeprep.local');student.set_password('Student@123');db.session.add(student)
    for n,k in [('Verbal Ability','verbal'),('DSA','dsa')]:
        if not Category.query.filter_by(name=n).first():db.session.add(Category(name=n,kind=k))
    db.session.commit()
    seed_topics(); seed_companies(); seed_tests(); seed_coding_bank(); seed_dsa(); seed_interviews(); seed_achievements()
