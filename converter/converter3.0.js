	// Init

	let selcode=0;
	$( function() {

			// create selectmenu 
	    $( "#code" ).selectmenu({
	    	change: function( event, data ) {
	    		change_code(data.item.value);
	    		additional_options();
	       }
	     })
	    .selectmenu( "option", "width", "auto" );
	 
	    $( "#mode" ).selectmenu({
	    	change: function( event, data ) {

	    		additional_options();

	    		if (selcode != 5) {
	    			reqenc(selcode);
	    		}
	    		else {
	    			reqjs();
	    		}
	       }
	     })
	    .selectmenu( "option", "width", "auto" )
	    .selectmenu("menuWidget")
	    .addClass("overflow");
	 
	    $( "#charset" ).selectmenu({
	    	change: function( event, data ) {
	    		reqenc(selcode);
	       }
	     })
	    .selectmenu( "option", "width", "auto" )
	      .selectmenu( "menuWidget" )
	      .addClass( "overflow" );
	 
	 		$( ".sort-option" ).checkboxradio().on( "change", function( event, ui ) {
	 			reqjs();
	 		} );

	 		$( ".uniq-option" ).checkboxradio().on( "change", function( event, ui ) {
	 			reqjs();
	 		} );

	    $('#hashing').css('display', 'none');
	    $('#options_sort').css('display', 'none');
	    $('#options_uniq').css('display', 'none');
	    change_code("0");

	    // event handler bind
	    $("#swap").on("click", function(event) { swap(); });
	    $("#Encode").on("input", function(event) { reqenc(0); });
	    $("#Decode").on("input", function(event) { reqenc(1); });
	    $("#Plain").on("input", function(event) { reqenc(2); });
	    $("#Text").on("input", function(event) { reqenc(3); });
	    $("#Encrypted").on("input", function(event) { reqenc(4); });
	    $("#Input").on("input", function(event) { reqjs(); });

  } );

	// ### Options ###
	// Code Event
	// 0 en/decode 1 hashing 2 en/decryption
	function change_code(code) {

		// input/ output display event
		$('#endecode').css('display', 'none');
		$('#hashing').css('display', 'none');
		$('#endecrypt').css('display', 'none');
		$('#translator').css('display', 'none');
		$("select[name='mode'] option").remove();

		// setting data
		switch(code) {
			case "0":
				selcode = 0;
				$('#endecode').css('display', 'block');
				option_data = {"":{"url":"URL","b64":"Base64","hex":"Hex"}}
				break
			case "1":
				selcode = 2;
				$('#hashing').css('display', 'block');
				option_data = {"자주 쓰는 메뉴":{"md5":"md5","sha256":"sha256","sha512":"sha512"},"전체 메뉴":{"md2":"md2","md4":"md4","sha1":"sha1","sha224":"sha224","sha384":"sha384","sha512/224":"sha512/224","sha3-224":"sha3-224","sha512/256":"sha512/256","sha3-256":"sha3-256","sha3-384":"sha3-384","sha3-512":"sha3-512","ripemd128":"ripemd128","ripemd160":"ripemd160","ripemd256":"ripemd256","ripemd320":"ripemd320","whirlpool":"whirlpool","tiger128,3":"tiger128,3","tiger160,3":"tiger160,3","tiger192,3":"tiger192,3","haval224,3":"haval224,3","haval128,5":"haval128,5","haval160,5":"haval160,5","haval192,5":"haval192,5","haval224,5":"haval224,5","haval256,5":"haval256,5"}}
				break	
			case "2":
				selcode = 3;
				$('#endecrypt').css('display', 'block');
				option_data = {"AES":{"aes-128-cbc":"AES-128-CBC","aes-192-cbc":"AES-192-CBC","aes-256-cbc":"AES-256-CBC"},"DES":{"des-ede-cbc":"DES-EDE-CBC","des-ede-ecb":"DES-EDE-EBC","des-ede3":"3DES","des-ede3-cbc":"3DES-CBC"},"ARIA":{"aria-128-cbc":"ARIA-128-CBC","aria-192-cbc":"ARIA-192-CBC","aria-256-cbc":"ARIA-256-CBC"},"CAMELLIA":{"camellia-128-cbc":"CAMELLIA-128-CBC","camellia-192-cbc":"CAMELLIA-192-CBC","camellia-256-cbc":"CAMELLIA-256-CBC"}};
				break
			case "3":
				selcode = 5;
				$('#translator').css('display', 'block');
				option_data = {"":{"reverse":"Reverse","rot13":"ROT13","sort":"Sort","uniq":'Unique'}};
				break
		}

		// change mode option event
		let option_text = "";
		for (const i in option_data ) {
			option_text += `<optgroup label="${i}">`;
			const property = option_data[i];
			for (const j in property) {
				option_text += `<option value="${j}">${property[j]}</option>`;
			}
			option_text += "</optgroup>";
		}

		$("#mode").append(option_text);
		$( "#mode" ).selectmenu("refresh");
	}

	function swap() {
		switch(selcode) {
			case 0:
				$("#Encode").val($("#Decode").val());
				reqenc(selcode);
				break
			case 2:
				$("#Plain").val($("#Hash").val());
				reqenc(selcode);
				break
			case 3:
				$("#Text").val($("#Encrypted").val());
				reqenc(selcode)
				break
			case 5:
				$("#Input").val($("#Output").val());
				reqjs()
				break
		}
	}

	function additional_options() {
		$('#options_sort').css('display', 'none');
	  $('#options_uniq').css('display', 'none');
	  if ($("#mode").val() == "sort") {
	  	$('#options_sort').css('display', 'block');
	  }
	  else if ($("#mode").val() == "uniq") {
	  	$('#options_uniq').css('display', 'block');
	  }
	}

	// ### Options End ###

	// ### Request and Response ###

	function getresult(formData) {
		let temp;
		//console.log(formData);
		$.ajax({
			url:"/enc.php",
			type:"POST",
			data:encodeURI(formData),
			async: false,
			success:function(data) {
				temp = data;
			},
			error: function(xhr,status) {
				console.log(xhr + ":" + status);
			}
		});

		return temp;
	}

	function reqenc(code) {
		console.log(code);
		let val;
		switch(code) {
			case 0:
				val = $("#Encode").val();
				break
			case 1:
				val = $("#Decode").val();
				break
			case 2:
				val = $("#Plain").val();
				break
			case 3:
				val = $("#Text").val();
				val = val + "&key=" + $("#Key").val() +"&IV=" + $("#IV").val();
				console.log(val);
				break
			case 4:
				val = encodeURIComponent($("#Encrypted").val());
				val = val + "&key=" + $("#Key").val() +"&IV=" + $("#IV").val();
				break
		}
		const formData = $("#test").serialize()+"&code="+code+"&data="+val;
		const result = getresult(formData);
		switch(code) {
			case 0:
				$("#Decode").val(result);
				break
			case 1:
				$("#Encode").val(result);
				break
			case 2:
				$("#Hash").val(result);
				break
			case 3:
				val = $("#Encrypted").val(result);
				break
			case 4:
				val = $("#Text").val(result);
				break
		}


	}

	function reqjs() {
		result = window[$("#mode").val()]();

		$("#Output").val(result);
	}

	// ### Request and Response End ###

	// ### reqjs ### 

	function reverse() {
		let result = ''
		const array = $("#Input").val();
		for ( i of array ) {
    	result = i + result;
		}

		return result;
	}
	
	function rot13() {
		let result = ''
		const alphabet = 'abcdefghijklmnopqrstuvwxyz';
		const array = $("#Input").val();
		for ( i in alphabet ) {
			result += "ROT["+i+"] => "
			for ( j of array ) {
				if (alphabet.indexOf(j.toLowerCase()) != -1 && alphabet.indexOf(j) != -1 ) {
					result += alphabet[(alphabet.indexOf(j)+parseInt(i))%26];
				}
				else if (alphabet.indexOf(j.toLowerCase()) != -1){
					result += alphabet[(alphabet.indexOf(j.toLowerCase())+parseInt(i))%26].toUpperCase();
				}
				else {
					result += j;
				}
			}
			result += "\n"
		}

		return result;
	}

	function sort() {
		let array=$("#Input").val().split('\n');
		if ($("#sort-rm-space").is(":checked")) {
			array = array.map(element => {
    			return element.trim();
			});
		}
		
		if ($("#sort-ignore-case").is(":checked")) {
			array.sort((a,b) => a.localeCompare(b));	
		}
		else {
			array.sort();
		}

		if ($("#sort-desc").is(":checked")) {
			array.reverse();
		}
		

		const result = array.join('\n');
		return result;
		}

	function uniq() {
		let array=$("#Input").val().split('\n');

		if ($("#uniq-rm-space").is(":checked")) {
			array = array.map(element => {
    			return element.trim();
			});
		}

		if ($("#uniq-ignore-case").is(":checked")) {
			array = Array.from(new Map(array.map(element => [element.toLowerCase(), element])).values());
		}
		else {
			array = Array.from(new Set(array));
		}
		
		const result = array.join('\n');
		return result;
	}

	// ### reqjs END ### 
