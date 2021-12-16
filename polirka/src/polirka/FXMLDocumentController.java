/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package polirka;

import com.sun.jndi.dns.DnsContextFactory;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import static java.lang.System.gc;
import static java.lang.System.in;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URL;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;
import static java.util.logging.Logger.global;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.concurrent.Task;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.scene.shape.Line;
import org.omg.CORBA.TIMEOUT;
import java.util.Scanner;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

/**
 *
 * @author Dejan
 */
public class FXMLDocumentController implements Initializable {

    public DataOutputStream dout2;
    public DataOutputStream dout;
    public DataOutputStream dout3;
    public DataOutputStream dout4;
    public DataInputStream in;
    public DataInputStream in2;
    public DataInputStream in3;
    public DataInputStream in4;
    private Label label;
    private Label pajton;
    @FXML
    private Label xosa;
    @FXML
    private Label yosa;
    private ComboBox combobrojploca;
    public String msg;
    public String yOsaKoordinata;
    public String zOsaKoordinata;
    public int x1;
    public int y1;
    public int x2;
    public int y2;
    @FXML
    private TextField textyosa;
    @FXML
    private Button okyosa;

    int yosavrednost;
    @FXML
    private Label zosa;
    @FXML
    private Button podesavanja;
    @FXML
    private Button startButton;
    @FXML
    private TextField brKomada;
    @FXML
    private TextField sirinaKomada;
    @FXML
    private TextField duzinaKomada;
    @FXML
    private Button stopButton;
    @FXML
    private Button homiranje;

    @Override
    public void initialize(URL url, ResourceBundle rb) {

        // TODO

        server task = new server();
        new Thread(task).start();

        test task1 = new test();
        new Thread(task1).start();

        yOsa task2 = new yOsa();
        new Thread(task2).start();

        zOsa task3 = new zOsa();
        new Thread(task3).start();

    }

    @FXML
    private void submit(ActionEvent event) throws IOException {

        yosavrednost = Integer.parseInt(textyosa.getText());
        System.out.println(yosavrednost);
        dout2.writeUTF(Integer.toString(yosavrednost));
        // String proba = "Ok";
        //dout2.writeUTF(proba);
    }

    @FXML
    private void podesavanja(ActionEvent event) throws IOException {

        Parent podesavanjaParent = FXMLLoader.load(getClass().getResource("podesavanja.fxml"));
        Scene podesavanjaScene = new Scene(podesavanjaParent);
        Stage window = (Stage) ((Node) event.getSource()).getScene().getWindow();
        window.setScene(podesavanjaScene);
        window.show();

    }
    


    @FXML
    private void startButton(ActionEvent event) {
        FileWriter writter = null;
        try {
            //String putanja = "C:/Users/Dejan/Desktop/testIzPrograma.txt";
            String putanja = "/home/pi/Desktop/testIzPrograma.txt";
            String kod = "";
            
            Integer komada = Integer.valueOf(brKomada.getText());
            Integer sirina = Integer.valueOf(sirinaKomada.getText());
            Integer duzina = Integer.valueOf(duzinaKomada.getText());
            
            int xKrajnja = 0;
            int yKrajnja = Integer.valueOf(yosa.getText());
            int zKrajnja = 0;
            
            for (int i = 0; i < komada; i++) {
                if (i > 0) {
                 yKrajnja = yKrajnja + sirina;
                kod = kod + "Y" + yKrajnja + "\n" + "Z" + Integer.valueOf(zosa.getText()) +"\n";
                }
                xKrajnja = Integer.valueOf(xosa.getText()) + duzina;
                zKrajnja = Integer.valueOf(zosa.getText()) + 3000;
                kod = kod + "X" + xKrajnja + "\n" + "Z" + zKrajnja + "\n" + "X" + xosa.getText() + "\n";
                
            }
            
            
            
            writter = new FileWriter(putanja, false);
            writter.write(kod);
            System.out.println("START BUTTON");
            dout2.writeUTF("start");
            System.out.println("POSLAO START");
        } catch (IOException ex) {
            Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            try {
                writter.close();
            } catch (IOException ex) {
                Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    @FXML
    private void stopDugme(ActionEvent event) throws IOException {
        dout2.writeUTF("stop");
        System.out.println("poslao STOP");
    }

    @FXML
    private void homiranjeDugme(ActionEvent event) throws IOException {
        
        dout2.writeUTF("nuliranje");
        System.out.println("nula");
    }

    public class server extends Task {

        public server() {
        }

        public void run() {

            try {

                System.out.println("STARTOVAN SOKET 1 port 10000");
                ServerSocket serverSocket = new ServerSocket(10000);
                Socket soc = serverSocket.accept();
                System.out.println("Receive new connection: " + soc.getInetAddress());
                dout = new DataOutputStream(soc.getOutputStream());
                in = new DataInputStream(soc.getInputStream());
            } catch (Exception e) {
                e.printStackTrace();
            }

            while (true) {

                try {
                    String msg = (String) in.readLine();
                    //dout.writeUTF("Thank You For Connecting.");
                    Platform.runLater(() -> {
                        xosa.setText(msg);
                    });
                } catch (IOException ex) {
                    Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
                }

            }

        }
//

        @Override
        protected Object call() throws Exception {
            throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        }
    }

    public class yOsa extends Task {

        public yOsa() {
        }

        public void run() {

            try {

                System.out.println("STARTOVAN SOKET 3 port 10002");
                ServerSocket serverSocket3 = new ServerSocket(10002);
                Socket soc3 = serverSocket3.accept();
                System.out.println("Receive new connection: " + soc3.getInetAddress());
                dout3 = new DataOutputStream(soc3.getOutputStream());
                in3 = new DataInputStream(soc3.getInputStream());
            } catch (Exception e) {
                e.printStackTrace();
            }

            while (true) {

                try {
                    String yOsaKoordinata = (String) in3.readLine();
                    //dout.writeUTF("Thank You For Connecting.");
                    Platform.runLater(() -> {
                        yosa.setText(yOsaKoordinata);
                    });
                } catch (IOException ex) {
                    Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
                }

            }


        }
//

        @Override
        protected Object call() throws Exception {
            throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        }
    }

    public class zOsa extends Task {

        public zOsa() {
        }

        @Override
        public void run() {

            try {

                System.out.println("STARTOVAN SOKET 4 port 10003");
                ServerSocket serverSocket4 = new ServerSocket(10003);
                Socket soc4 = serverSocket4.accept();
                System.out.println("Receive new connection: " + soc4.getInetAddress());
                dout4 = new DataOutputStream(soc4.getOutputStream());
                in4 = new DataInputStream(soc4.getInputStream());
            } catch (Exception e) {
                e.printStackTrace();
            }

            while (true) {

                try {
                    String zOsaKoordinata = (String) in4.readLine();
                    
                    Platform.runLater(() -> {
                        zosa.setText(zOsaKoordinata);
                    });
                    //System.out.println(zOsaKoordinata);
                } catch (IOException ex) {
                    Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
                }

            }

        }
//

        @Override
        protected Object call() throws Exception {
            throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        }
    }

    public class test extends Task {

        public test() {
        }

        public void run() {
            try {

                System.out.println("STARTOVAN SOKET 2 port 10001");
                ServerSocket serverSocket2 = new ServerSocket(10001);
                Socket soc2 = serverSocket2.accept();
                System.out.println("Receive new connection: " + soc2.getInetAddress());
                dout2 = new DataOutputStream(soc2.getOutputStream());
                DataInputStream in2 = new DataInputStream(soc2.getInputStream());
                while (true) {

                    
                }
            } catch (IOException ex) {
                Logger.getLogger(FXMLDocumentController.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

        @Override
        protected Object call() throws Exception {
            throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        }

    }
}
