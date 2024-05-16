// file written by Connor Ettinger (Team Axoltol) for challenge 2
/* README - File Use Instructions
 * 1. Replace all four instances of "Example"
 * (on lines 24, 111, and 113) with the name of the
 * .class file (e.g., if the file is Challenge.class,
 * replace Example with Challenge)
 * 
 * 2.(in main) Comment out function calls
 * for info you don't want (i.e., if you
 * don't care about the constructor,
 * comment out printConstructor())
 * 
 * 3. Compile and run!
 */
import java.lang.reflect.*;
class infoObtainer {
    public static void main(String[] args) throws Exception{
        // README: I put everything into individual funtions, 
        // so that you can just comment out fucntion calls
        // for anything you don't want to see/do

        // create the object to be inspected
        // TODO: replace "Example" with the name of the .class file
        Example ex = new Example();

        // create a class file and store object in it (for finding class info)
        Class c = ex.getClass();

        // print all of the SuperClasses of the class
        // the second arguement determines if we print all of c's super classes.
        // if true, print all of c's ancestors, if false print only c's direct super
        printSuperClass(c, true);

        // print the constructor of the class
        // TODO: figure out why we need this
        printConstructor(c);

        // print the methods of the class
        // the second arguement is true if you want to print hidden methods
        // and false if you just want public methods
        printMethods(c, true);

        // print all of the fields of the class
        printFields(ex);
    }

    private static void printSuperClass(Class c, boolean printAllSups) throws Exception{
        System.out.println("\nGrabbing Super Class");
        Class sup = c.getSuperclass();

        // if the super class of c is the Object class,
        // it doesn't have any super classes, so print that
        if (sup.getName() == "java.lang.Object") {
            // obviously, the Object Class is the super of all classes
            // but since we don't care about it, it's easier to just say
            // that it doesn't have a super class
            System.out.println("This class has no super class");
            System.out.println("\n---------------------------------------");
        } else { // c has a super class
            // print the super class of c
            System.out.println("The super class of " + c.getName() + " is " + sup.getName());

            // if we want to print all of ancestors of c
            // (aka if printAllAncestors is true)
            // make sure that sup isn't the Object class,
            // because if it is then we're at the most superior class
            while (sup.getName() != "java.lang.Object" && printAllSups){
                // print the super class of sup
                System.out.println("The super class of " + sup.getName() + " is " + sup.getSuperclass().getName());
                // set sup equal to it's super class
                sup = sup.getSuperclass();
            }
            System.out.println("\n---------------------------------------");
        }
    }

    private static void printConstructor(Class c){
        System.out.println("\nGrabbing Constructor");
        // figure out if there is a constructor
        try{
            Constructor con = c.getConstructor();
            System.out.println(con);
        } catch (Exception e){
            System.err.println("Constructor Not There");
            System.err.println(e);
        }
        System.out.println("\n---------------------------------------");
    }

    private static void printMethods(Class c, boolean showHidden) {
        System.out.println("\nGrabbing Methods");

        if(showHidden){
            // get all methods
            Method[] allMethods = c.getDeclaredMethods();
            // print them
            for (Method m : allMethods){
                System.out.println(m);
            }
        } else{
            // get just the public methods
            Method [] methods = c.getMethods();
            // print them
            for (Method m : methods){
                System.out.println(m);
            }
        }
        System.out.println("\n---------------------------------------");
    }

    private static void printFields(Example ex) throws Exception{
        System.out.println("\nGrabbing Fields");
        Field[] fields = Example.class.getDeclaredFields();
        int field_num = 0;
        for (Field field : fields){
            fields[field_num].setAccessible(true);
            field.setAccessible(true);
            System.out.println("field "+ field_num + ": " + field);
            try {
                System.out.println("field "+ field_num + " value: " + field.get(ex) + "\n");
            } catch (Exception e) {
                System.out.println("cannot print value of this field, sorry\n");
            }
            field_num++;
        }
    }
}