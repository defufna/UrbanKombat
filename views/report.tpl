% rebase('base.tpl', title='Report')

<div class="gp">
%if name:
	<h1>{{name}}</h1>
%end
	<h2>{{title}}</h2>
	<p>
		<strong>Game report:</strong>
		<ul>
		%for event in events:
			<li>{{event}}</li>
		%end
		</ul>
	</p>
</div>