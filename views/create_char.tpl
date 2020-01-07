<fieldset>
    <legend>Character creation</legend>
    <label>Name:</label>
    <input type="text" name="char_name">
%if defined("team"):
    <input type="hidden" name="team" value="{{team}}">
%end
    <label>Class</label>
    <select name="cls">
        <option>Human</option>
        <option>Zombie</option>
    </select>
</fieldset>
