% rebase('base.tpl', title='Report')

<div class="gp">
%if name:
	<h1>{{name}}</h1>
%end
	<h2>{{title}}</h2>
	<a href="/">Create new game</a>
	<p>		
		<strong>Game report:</strong>
		<ul>
		%for event in events:
			<li>{{event}}</li>
		%end
		</ul>
	</p>
	<p>
	    <strong>
	        You can share this report with others by copying the url,
	        but note that it won't live forever, older reports are deleted.
	    </strong>
	</p>
</div>