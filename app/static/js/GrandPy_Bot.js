$(function() {
	var loading = $("<p></p>").html($("<img>", {src: "../static/images/loading.gif", alt: "loading..."}))

	$("#user_form").on("submit", function(event) {
		var user_message = $("#user_message").val();
		event.preventDefault();
		event.stopPropagation();
		var dialog_box = $("#dialog_box");
		$("<p></p>").text(user_message).appendTo(dialog_box);
		var request = new XMLHttpRequest();
		request.onreadystatechange = function() {
			if (this.readyState == XMLHttpRequest.DONE) {
				loading.remove()
				if (this.status == 200) {
					var result = JSON.parse(this.responseText);
					if (result.status == "OK") {
						$("<p></p>").text(result.address).appendTo(dialog_box)
						$("<p></p>").html($("<img>", {src: result.static_map_url, alt: "carte du lieu"})).appendTo(dialog_box)
						$("<p></p>").text(result.story).appendTo(dialog_box)
						dialog_box.scrollTop(dialog_box[0].scrollHeight);
					} else if (result.status == "address_not_found") {
						$("<p></p>").text(result.message).appendTo(dialog_box)
					}
				} // else throw error?
			} else {
				dialog_box.append(loading);
				dialog_box.scrollTop(dialog_box[0].scrollHeight);
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