// this file was written by Connor Ettinger (Team Axoltol) for challenge 2
/* README - File Use Instructions:
 * 1. Replace all four instances of "Example"
 * (on lines 30, 34, and 49) with the name of
 * the.class file (e.g., if the file is
 * Challenge.class, replace Example
 * with Challenge)
 * 
 * 2. go to line 39, and replace the first arguement
 * with the number of the field you want to change
 * (e.g, if you want to modify the 2nd field,
 * change the first arguement to 1)
 * 
 * 3. replace the 2nd arguement with the value you
 * want to change the field to
 *     3.1 if the field's type isn't an int,
 *     make sure to go to the function (line 49)
 *     declaration and change the type as well
 * 
 * 4. go to line 44, and replace the arguement with the
 * with the name of the method you want to run
 * 
 * 5. Compile and Run!
*/
import java.lang.reflect.*;
public class fieldModifier {
    public static void main(String[] args) throws Exception {
        // create the object we're dealing with
        // TODO: replace "Example" with the name of the .class file
        Example ex = new Example();
        Class c = ex.getClass();

        // generate list of fields in the class
        Field [] fields = Example.class.getDeclaredFields();

        // change the field to the specified value
        // TODO: replace "field_num" with the number of the field you want to change
        // TODO: replace "field_val" with the value you want to change the field to
        fields = changeField(0, 1000, ex, fields);
        // for more info on what the arguements do, ask Connor

        // finally, run the class method with the modified field
        // TODO: put the name of the method you wish to execute as the arguement
        Method m = c.getDeclaredMethod("Insert Name Here");
        m.setAccessible(true);
        m.invoke(ex);
    }

    private static Field[] changeField(int field_num, int field_val, Example cls, Field[] fields) throws Exception {
        fields[field_num].setAccessible(true);
        fields[field_num].set(cls, field_val);
        return fields;
    }
}