$(function() {
	$("#user_form").on("submit", function(event) {
		var user_message = $("#user_message").val();
		event.preventDefault();
		event.stopPropagation();
		var request = new XMLHttpRequest();
		var url = window.location.href + "getResponse?user_message=" + user_message;
		request.open("GET", url);
		request.send();
//		jQuerry.get("https://fr.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord=48.8748465|2.3504873&gsradius=10000&gslimit=10");
//		$.ajax({
//			url: window.location.hostname + "/getResponse",
//			data: {
//				user_message: "test"
//			},
//			type: "GET",
//			dataType: "json",
//		}).done(function(json) {
//			alert("done");
//		}).fail(function(xhr, status, errorThrown) {
//			alert("Sorry, there was a problem in the request");
//		});
		$('#user_form').trigger("reset");
	})
})