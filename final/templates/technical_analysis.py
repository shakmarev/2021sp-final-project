{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Fundamental{% endblock %}</h1>
{% endblock %}

{% block content %}
According to analysis based on {{ model }} model inner value of {{ ticker }} is approximately {{ total }}.
<br>
Years of payment: {{ years }}
<br>
Discount rate: {{ rate }}
<br/>
Growth rate: {{ growth }}
<br/>
Terminal value is {{ terminal }}
<br/>
Observations are:
{% for o in observations %}
  <li>{{ o }}</li>
{% endfor %}

<script>
window.onload = function () {

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	theme: "light2",
	title:{
		text: "Observations"
	},
	data: [{
		type: "line",
      	indexLabelFontSize: 16,
		dataPoints: {{ points|safe }}
	}]
});
chart.render();

}
</script>

<div id="chartContainer" style="height: 300px; width: 100%;"></div>
<script src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>

{% endblock %}
