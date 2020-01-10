<fieldset>
    <legend>Character creation</legend>
    <label>Name:</label>
    <input type="text" name="char_name">
%if get("pick_team", False):
    <label>Team:</label>
    <select name="team">
        %for team in game.teams:
            <option value="{{team}}">{{team}}</option>
        %end
    </select>
%end
    <label>Class:</label>
    <select name="cls">
        <option>Human</option>
        <option>Zombie</option>
    </select>
</fieldset>
