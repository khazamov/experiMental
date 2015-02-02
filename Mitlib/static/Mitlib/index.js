var jData = {
			labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "November", "December"],
			datasets: [
				{
					data: [[11], [23]],
					fillColor: "rgba(151,87,25,0.2)",
					strokeColor: "#FF5A5E",
					pointColor: "rgba(220,220,220,1)",
            		pointStrokeColor: "#fff",
            		pointHighlightFill: "#fff",
            		pointHighlightStroke: "rgba(220,220,220,0.3)",
					label: "Portfolio performance"
				},
				{
					data: [[41], [13]],
					fillColor: "rgba(51,187,205,0.2)",
					strokeColor: "#5AD3D1",
					pointColor: "rgba(151,187,205,1)",
            		pointStrokeColor: "#fff",
            		pointHighlightFill: "#fff",
            		pointHighlightStroke: "rgba(151,187,205,0.3)",
					label: "Fund performance"
				}
					]
			};
			window.onload = function(){
				var ctx = document.getElementById("chart-area").getContext("2d");
				window.myPolarArea = new Chart(ctx).Line(jData, {
					responsive:true
				});
			};



