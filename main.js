

var _id;
var _typ;
var _intervallIndex;
var _intervallText = "";

var _utforPageReload = false;



var _aktivaBokningarValtDatum = 0;
var _aktivaBokningarTotalt = 0;


$(document).ready(function() {




function utforBoka(){
	var datum = document.getElementById('datum').value;
	var moment = document.getElementById('moment').value;
	encodeURIComponent(moment);





	var resp = $.ajax({
   		url: '/ajax/ajax_resursbokning.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		"op" : "boka",
      		"datum" : datum, //ÅÅ-MM-DD
      		"id" : _id, //sal
      		"typ" : _typ, //'RESURSER_LOKALER'
      		"intervall" : _intervallIndex, // Tidsinterval 0-5
      		"moment" : moment, //Kommentar
      		"flik" : "FLIK-0017" //Hus
      	}),
      	dataType: "html",
      	async:false
   	}).responseText;








	if (resp != "OK"){
		$("#boka-error-div").html(resp);
	}
	else{
		if (_utforPageReload){
			var dNow = new Date();
			var timeMillis = dNow.getTime();
			window.location.href=window.location.href+"&reloadtime="+timeMillis;
		}
		else{
			$( "#boka-dialog" ).dialog( "close" );
			hamtaResursBokningar();
			hamtaMinaBokningar();
		}
	}


}

function hamtaMinaBokningar(){

	var datum = document.getElementById('datum').value;

	var resp = $.ajax({
   		url: '/minaresursbokningar.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		"flik" : "FLIK-0017",
      		"datum" : datum
      	}),
      	dataType: "html",
      	async:false
   	}).responseText;

	$("#minaresursbokningar-resultat").html(resp);
}

function boka(id, typ, intervallIndex, intervallText){

	if (!kollaMaxAntalBokningar()){
		return;
	}

	_id = id;
	_typ = typ;
	_intervallIndex = intervallIndex;
	_intervallText = intervallText;




		var sign = "ac8240";

		$("#boka-content").html(
			"<p>Resurs: <b>"+id+"</b></p>"+
			"<p>Tid: <b>"+intervallText+"</b></p>"+
			"<p>Signatur: <b>"+sign+"</b></p>"
		);

		$("#boka-error-div").html("");

		_utforPageReload = false;
		$("#boka-dialog").dialog( "open" );

		$("#boka-dialog").height("auto");


}

function avboka(id){

	var resp = $.ajax({
   		url: '/ajax/ajax_resursbokning.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		"op" : "avboka",
      		"bokningsId" : id
      	}),
      	dataType: "html",
      	async:false
   	}).responseText;

	if (resp == "OK"){
		//alert("Du har nu avbokat grupprummet.");
		hamtaResursBokningar();
		hamtaMinaBokningar();
	}
	else{
		alert(resp);
	}
}

function konfirmera(bokningsId){

	var resp = $.ajax({
   		url: '/ajax/ajax_resursbokning.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		"op" : "konfirmera",
      		"flik" : "FLIK-0017",
      		"bokningsId" : bokningsId
      	}),
      	dataType: "html",
      	async:false
   	}).responseText;

	if (resp == "OK"){
		alert("Du har nu bekräftat bokningen.");
		hamtaResursBokningar();
		hamtaMinaBokningar();
	}
	else{
		alert(resp);
		hamtaResursBokningar();
		hamtaMinaBokningar();
	}
}

function hamtaResursBokningar(){

	var datum = document.getElementById('datum').value;

	var resp = $.ajax({
   		url: '/ajax/ajax_resursbokning.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		"op" : "hamtaBokningar",
      		"datum" : datum,
      		"flik" : "FLIK-0017"
      	}),
      	dataType: "html",
      	async:false
   	}).responseText;

	$('#resultat-div').html(resp);


	$(".tooltip").qtip({
		style: { name: 'blue', tip: true },
		position: {
	      	corner: {
	       		target: 'topRight',
	         	tooltip: 'bottomLeft'
	      	}
	   	}
	});
}

function formatera_datumfalt(){

	var datum = formatera_datum(document.getElementById('datum').value);
	document.getElementById('datum').value = datum;

	hamtaResursBokningar();
	hamtaMinaBokningar();
}

function satt_datum(datum){

	datum = formatera_datum(datum);
	document.getElementById('datum').value = datum;

	hamtaResursBokningar();
	hamtaMinaBokningar();
}

function open_login(){
	$("#dialog-login").dialog( "open" );
}

function resursbokning_do_login(){

	var login_username = document.getElementById('resursbokning_do_login_username').value;
	var login_password = document.getElementById('resursbokning_do_login_password').value;

	if (!login_username || login_username.length < 1){
		alert("Du måste ange ditt användarnamn.");
		return;
	}

	var resp = $.ajax({
   		url: 'ajax/ajax_login.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		username : login_username,
      		password : login_password
      	}),
      	dataType: 'html',
      	async:false
   	}).responseText;

	if (resp != 'OK'){
		alert(resp);
		return;
	}
	else{

		$("#dialog-login").dialog( "close" );

		do_page_reload();

		//hamtaResursBokningar();
		//hamtaMinaBokningar();
	}
}

function do_page_reload(){

	var dNow = new Date();
	var timeMillis = dNow.getTime();
	window.location.href=window.location.href+"&reloadtime="+timeMillis+"&flik=FLIK-0017";

}

function do_login_boka(){

	var login_username = document.getElementById('boka_login_username').value;
	var login_password = document.getElementById('boka_login_password').value;

	if (!login_username || login_username.length < 1){
		alert("Du måste ange ditt användarnamn.");
		return;
	}

	var resp = $.ajax({
   		url: 'ajax/ajax_login.jsp',
   		global: false,
      	type: "GET",
      	data: ({
      		username : login_username,
      		password : login_password
      	}),
      	dataType: 'html',
      	async:false
   	}).responseText;

	if (resp != 'OK'){
		alert(resp);
		return;
	}
	else{

		// Titta så vi har tillgång till den fliken vi står på. Annars visar vi en alert och
		// laddar bara om sidan.
		var flikResp = $.ajax({
	   		url: 'ajax/ajax_resursbokning.jsp',
	   		global: false,
	      	type: "GET",
	      	data: ({
	      		op : "harTillgangTillFlik",
	      		flik : "FLIK-0017"
	      	}),
	      	dataType: 'html',
	      	async:false
	   	}).responseText;

		if (flikResp != "OK"){
			alert("Du har inte rättigheter att boka denna resursflik: FLIK-0017");
			do_page_reload();
			return;
		}


		var sign = $.ajax({
	   		url: 'ajax/ajax_session.jsp',
	   		global: false,
	      	type: "GET",
	      	data: ({
	      		op : "anvandarId"
	      	}),
	      	dataType: 'html',
	      	async:false
	   	}).responseText;

		$("#boka-content").html(
			"<p>Resurs: <b>"+_id+"</b></p>"+
			"<p>Tid: <b>"+_intervallText+"</b></p>"+
			"<p>Signatur: <b>"+sign+"</b></p>"
		);

		$("#boka-dialog-login").dialog( "close" );

		$("#boka-dialog").dialog( "open" );

		$("#boka-dialog").height("auto");

		hamtaResursBokningar();
		hamtaMinaBokningar();
	}



}
