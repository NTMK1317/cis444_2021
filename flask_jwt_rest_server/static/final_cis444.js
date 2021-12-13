var jwt = null
function secure_get_with_token(endpoint, data_to_send, on_success_callback, on_fail_callback){
	console.log(data_to_send);
	xhr = new XMLHttpRequest();
	function setHeader(xhr) {
		xhr.setRequestHeader('Authorization', 'Bearer:'+jwt);
	}
	function get_and_set_new_jwt(data){
		console.log(data);
		jwt  = data.token
		on_success_callback(data)
	}
	$.ajax({
		url: endpoint,
		data : data_to_send,
		type: 'GET',
		datatype: 'json',
		success: on_success_callback,
		error: on_fail_callback,
		beforeSend: setHeader
	});
}
function send_form(){
			var inun = $('#in_name').val();
			var inpw = $('#in_word').val();
			var count = 0;

			if(inun.length == 0 || inpw.length == 0){
                                $('#fail').show();

                                setInterval( function(){
                                        count = count + 1;
                                        if(count == 5){
                                                $('#fail').hide();
                                        }
                                }, 500);
                                return false;
			}else{
				$.post("/open_api/login", { "firstname":$('#in_name').val(), "password":$('#in_word').val()},
                       			function(data, textStatus) {
						if(data.authenticated === false){
							//$('#mydiv').html("HI");
							$('#invalid').show();
							setInterval( function(){
                                        			count = count + 1;
                                        			if(count == 5){
                                                			$('#invalid').hide();
                                        			}
                                			}, 500);
						}else{
							console.log(data.authenticated);
							//this gets called when browser receives response from server
							console.log(data.token);
							//Set global JWT
							jwt = data.token;
							//make secure call with the jwt
							//get_books();
							$('#login').hide();
							$('#signup').hide();
							$('#divchatbox').show();
							document.getElementById("chatbttn").style.display = "block";
						}
					}, "json").fail( function(response) {
						//this gets called if the server throws an error
						console.log("error");
						console.log(response);
				});
			}
			return false;
}
function send_up(){
                        var upun = $('#up_name').val();
                        var uppw = $('#up_word').val();
			var count = 0;

			if(upun.length == 0 || uppw.length == 0){
				$('#fail').show();

				setInterval( function(){
					count = count + 1;
                                	if(count == 5){
                                        	$('#fail').hide();
                                	}
                        	}, 500);
				return false;
			}else{
				$.post("/open_api/addUser", { "username":upun, "password":uppw},
                                	function(data) {
                                        	$('#success').show();
                                	}, "json");

                                setInterval( function(){
                                        count = count + 1;
                                        if(count == 5){
                                                $('#success').hide();
                                        }
                                }, 500);
				return false;				
			}
                        return false;
}
function buy_book(){
			var db_book_id = $('#db_books').val();
			//$('#mydiv').html(db_book_id);
			secure_get_with_token("/secure_api/purchase", {"book_id" : db_book_id} ,
				function(data){
					console.log("purchased book");
					$('#books').hide();
					$('#thanks').show();
				}, function(err){ console.log(err) });
			return false;
}
function send_msg(){
	var user_msg = $('#msg').val();

	if(!user_msg || !user_msg.trim()){
		alert("Please type something in.");
		return false;
	}

	//$('#mydiv').html(user_msg);
	
	secure_get_with_token("/secure_api/savemessage", {"user_msg_sent" : user_msg} ,
		function(data){
			console.log("sent message");
		}, function(err){ console.log(err) });

	return false;
}
