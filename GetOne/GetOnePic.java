/**
 * Created by YeXiaoRain on 2014/12/7.
 */

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Scanner;

public class GetOnePic {
    Socket socket;
    BufferedReader br;
    PrintWriter pw;
    public static boolean saveUrlAs(String fileUrl, String savePath)
    {
        try {
            URL url = new URL(fileUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            DataInputStream in = new DataInputStream(connection.getInputStream());

            DataOutputStream out = new DataOutputStream(new FileOutputStream(savePath));


            byte[] buffer = new byte[4096];
            int count = 0;
            while ((count = in.read(buffer)) > 0)
            {
                out.write(buffer, 0, count);
            }
            out.close();
            in.close();
            connection.disconnect();
            return true;

        } catch (Exception e) {
            System.out.println(e + fileUrl + savePath);
            return false;
        }
    }
    private String getBackMsg(BufferedReader br){
        String strFromServer="";
        String nextLine;
        try {
            while((nextLine = br.readLine())!=null){//some times it stopped here
                strFromServer+=nextLine;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return strFromServer;
    }
    private String connectAndGetURL(String ip,int port,int picIndex){
        String sendStr="GET /one/vol."+picIndex+" HTTP/1.1\r\nHost: wufazhuce.com\r\n\r\n";
        try {
            socket = new Socket(ip, port);
            //System.out.println("Socket=" + socket);
            br = new BufferedReader(new InputStreamReader(
                    socket.getInputStream()));
            pw = new PrintWriter(new BufferedWriter(new OutputStreamWriter(
                    socket.getOutputStream())));
            pw.println(sendStr);
            pw.flush();

            String bkmsg=getBackMsg(br);
            int picst=bkmsg.indexOf("<div class=\"one-imagen\">");
            String subStr=bkmsg.substring(picst,picst+100);
            return subStr.substring(subStr.indexOf("http://"), subStr.indexOf(".jpg") + 4);
        } catch(ConnectException e){
            System.out.println("link error");
        }catch (Exception e) {
            System.out.println(e.getMessage());
            //e.printStackTrace();
        } finally {
            try {
                br.close();
                pw.close();
                socket.close();
            } catch (IOException e) {
                System.out.println("IOException"+e.getMessage());
                //e.printStackTrace();
            }catch (Exception e) {
                System.out.println("Exception"+e.getMessage());
                //e.printStackTrace();
            }
        }
        return "";
    }
    public static void main(String[] args) {
        Scanner scan=new Scanner(System.in);
        GetOnePic myOne=new GetOnePic();
        String webSite="wufazhuce.com";
        int port=80;
        int stpic=839,enpic=888;
        stpic=scan.nextInt();
        enpic=scan.nextInt();
		
        System.out.println("------Start------");
        try {
            InetAddress echoAddress;
            echoAddress = InetAddress.getByName(webSite);
            int i;
            String [] piclinklist= new String[enpic-stpic+1];
            for(i=stpic;i<=enpic;i++){
            	piclinklist[i-stpic]=myOne.connectAndGetURL(echoAddress.getHostAddress(), port,i);
            	System.out.println(i+":"+piclinklist[i-stpic]);            	
            }
            System.out.println("------Download------");
            for(i=stpic;i<=enpic;i++){
            	String savePath="E:/one/"+i+".jpg";
                saveUrlAs(piclinklist[i-stpic],savePath);
                System.out.println(i+":\t"+piclinklist[i-stpic]+"\t->\t"+savePath);
            }
        }catch (UnknownHostException e) {
            System.out.println(e.getMessage());
        }//get Address
        System.out.println("------Finish------");
    }
}
