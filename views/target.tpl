<select name="target">\\
%if get("include_self", False):
<option value="">self</option>\\
%end
%if not is_zombie:
    %include("target/a_zombie.tpl")
    %include("target/player_options.tpl", players=zombies)
    %include("target/player_options.tpl", players=humans)    
%else:
    %include("target/player_options.tpl", players=humans)
    %include("target/player_options.tpl", players=zombies)
    %include("target/a_zombie.tpl")
%end
</select>