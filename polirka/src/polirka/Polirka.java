/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package polirka;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.fxml.FXMLLoader;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.shape.Line;
import javafx.stage.Stage;

/**
 *
 * @author Dejan
 */
public class Polirka extends Application {
    
    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("FXMLDocument.fxml"));
        
        Scene scene = new Scene(root);

         stage.setTitle("HANS");
        stage.setScene(scene);
        stage.show();
        
        stage.setOnCloseRequest(e -> System.exit(0));
    }

    
    // * @param args the command line arguments
    // */
    public static void main(String[] args) {
        launch(args);
        
    }
    

        
        
    
    
}
