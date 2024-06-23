Solar System Classification is a rule-based expert system which takes a json file, declares facts based on data in the file, and proceeds to classify the facts as a planet,
dwarf planet, asteroid, inner system comet, outer system comet, and/or a Kuiper Belt Object (KBO).

Besides creating facts from a file, you can also manually enter a Fact by providing data in the python shell this way:
<pre>
engine.declare(Fact(name="<name>", orbits="sun"|"<name>", min_dist=<AU from sun>|<KM from parent>, max_dist=<AU from sun>|<KM from parent>, diameter=<KM diameter>,
                    mass=<10^24 KG>, shape="round"|"irregular")
</pre>
After which you would execute "engine.run()".

Data in the file has the format:
<pre>
{"name": "<name>", "orbits": "sun"|"<name>", "min_dist": <number>, "max_dist": <number>, "diameter": <number>, "mass": <number>,
 "shape": "round"|"irregular"}
</pre>

The code uses experta for the rules:
<ul>
  <li>https://pypi.org/project/experta/</li>
  <li>https://github.com/nilp0inter/experta</li>
  <li>https://experta.readthedocs.io/en/latest/index.html</li>
</ul>
<br>
Note: The goal of this project is not accuracy, but demonstration of a concept. Some classification rules are a simplication of what is otherwise complex or obscure principles.
For example, I used the mass of the Moon to differentiate planet and dwarf planet. I used the aphelion to classify inner system comets. 
