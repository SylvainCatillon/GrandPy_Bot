$(function() {
	$("#user_form").on("submit", function(event) {
		var user_message = $("#user_message").val();
		event.preventDefault();
		event.stopPropagation();
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (this.readyState == XMLHttpRequest.DONE) {
				if (this.status == 200) {
					var result = JSON.parse(this.responseText);
					var dialog_box = $("#dialog_box")
					var answer = "<p>"+result.address+"</p><p><img src='"+result.static_map_url+"' alt='carte du lieu'></p><p>"+result.story+"</p>";
					dialog_box.append(answer);
					dialog_box.scrollTop(dialog_box[0].scrollHeight);
				}
			}
		}
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