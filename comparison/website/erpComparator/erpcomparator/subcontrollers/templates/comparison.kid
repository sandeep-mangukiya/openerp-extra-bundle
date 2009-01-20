<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#" py:extends="../../templates/master.kid">

<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title>Comparison</title>
    
    <script type="text/javascript" src="/static/javascript/comparison.js"></script>
    
</head>
<body>
    <div class="mattblacktabs">
		<ul>
	    	<li id="current">
	    		<a href="#" onclick="window.location.href='/comparison'">
	    			<span>Comparison</span>
	    		</a>
	    	</li>
	    	<li>
	    		<a href="#" onclick="window.location.href='/softwares'">
	    			<span>Software</span>
	    		</a>
	    	</li>
	    	<li>
	    		<a href="#" onclick="window.location.href='/about'">
	    			<span>About</span>
	    		</a>
	    	</li>
	    	<li>
	    		<a href="#" onclick="window.location.href='/graph'">
	    			<span>Graph</span>
	    		</a>
	    	</li>
	    	<li>
	    		<a href="#" onclick="window.location.href='/login'">
	    			<span>Login</span>
	    		</a>
	    	</li>
	    	<li>
	    		<a href="#" onclick="window.location.href='/login/logout'">
	    			<span>Logout</span>
	    		</a>
	    	</li>
	  	</ul>
	</div><br/>
	<div id="selection">
		<table>
			<tr>
				<td class="label">
					You can compare among following Products : 
				</td>
			</tr>
		</table>
		<table name="item_list" id="item_list">
			<tr py:if="selected_items">
				<td py:for="label in titles">
					<input id="${label['id']}" type="checkbox" checked="${tg.selector(label['sel'])}" class="grid-record-selector">${label['name']}</input>
				</td>
			</tr>
			<tr py:if="not selected_items">
				<td py:for="label in titles">
					<input id="${label['id']}" type="checkbox" checked="true" class="grid-record-selector">${label['name']}</input>
				</td>
			</tr>
		</table>
		<br/>
		
		<button type='button' onclick="getRecords()">Compare</button>
	</div><br/>
	<div id="open_comp">
		<span id="comparison_tree"/>
		<script type="text/javascript">
        	var comparison_tree = new TreeGrid('comparison_tree');
        	
        	//comparison_tree.options.onbuttonclick = on_button_click;
        	comparison_tree.setHeaders(${ustr(headers)});
        	comparison_tree.setRecords('${url}', ${ustr(url_params)});
        	
        	comparison_tree.render();
        </script>
	</div>
	<div style="text-align: right; color: #993300;"><i>Note: ( ) value shows number of vote(s).</i></div>
</body>
</html>



