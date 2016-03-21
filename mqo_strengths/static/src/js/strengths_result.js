/*
 *    MQO Strengths JS
 *
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Affero General Public License as
 *    published by the Free Software Foundation, either version 3 of the
 *    License, or (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Affero General Public License for more details.
 *
 *    You should have received a copy of the GNU Affero General Public License
 *    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

$(document).ready(function () {
    'use strict';
    console.debug("[mqo_strengths] Strengths Result JS is loading...");

	var d3data = JSON.parse($('#d3bar').attr("d3data"));

	nv.addGraph(function() {
		var chart = nv.models.multiBarHorizontalChart()
			.x(function(d) { return d.label })
			.y(function(d) { return d.value })
			.margin({top: 30, right: 120, bottom: 50, left: 275})
			.showValues(true)
			.tooltips(true)
			.showControls(false)
			.forceY([0, 5]);

		chart.yAxis
			.tickFormat(d3.format(',.2f'));

		d3.select('#d3bar svg')
			.datum(d3data)
			.transition().duration(500).call(chart);

		nv.utils.windowResize(chart.update);

		return chart;
	});
	
    console.debug("[mqo_strengths] Strengths Result JS loaded!");
});