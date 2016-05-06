package data_frame;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.sql.*;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.Properties;

public class Delay_Box_plot {
	
	static Connection connection;
	public static Properties props;
	
	public static void readProperties() throws IOException {
		props = new Properties();
		FileInputStream in = new FileInputStream("database.properties");
		props.load(in);
		in.close();
	}
	
	public static void openConnection() throws SQLException, IOException
	{
		String drivers = props.getProperty("jdbc.drivers");
		if (drivers != null) System.setProperty("jdbc.drivers", drivers);

		String url = props.getProperty("jdbc.url");
		String username = props.getProperty("jdbc.username");
		String password = props.getProperty("jdbc.password");

		connection = DriverManager.getConnection( url, username, password);
	}
	
	public static String[] get_web_list(String in_file) throws IOException{
		String[] web_list = new String[200];
		@SuppressWarnings("resource")
		BufferedReader br = new BufferedReader(new FileReader(in_file));
		String line;
		String[] s;
		int i=0;
		while((line=br.readLine())!=null){
			s=line.split(" ");
			web_list[i]=s[0];
			i++;
		}
		return web_list;
	}
	
	public static boolean in_list(String web, String[] list){
		for(int i=0;i<list.length;i++){
			if(list[i]!=null && list[i].equals(web))
				return true;
		}
		return false;
	}
	
	public static void get_box_data(String out_file, String[] web_list)throws SQLException, IOException{
		Statement stat = connection.createStatement();
		
		File out = new File(out_file);
		FileOutputStream fos = new FileOutputStream(out);
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));
		int size=0;
		double[] delays = new double[1206];
		double total=0;
		int index=0;
		double mean,median,min,max,percent25,percent75;
		for(int i=0;i<web_list.length;i++){
			if(web_list[i]!=null){
				ResultSet result = stat.executeQuery("SELECT * FROM delay_data WHERE dest='"+web_list[i]+
						"' order by delay");
				min=0;
				while(result.next()){
					if(index==0) min=result.getDouble(3);
					delays[index] = result.getDouble(3);
					total+=delays[index];
					index++;
				}
				max=delays[index-1];
				size = index;
				mean = total/size;
				if(size%2==0){
					median = (delays[(size/2)-1] + delays[size/2])/2;
					percent25 = (delays[(size/4)-1] + delays[size/4])/2;
					percent75 = (delays[(size*3/4)-1] + delays[size*3/4])/2;
				}else{
					median = delays[(size-1)/2];
					percent25 = delays[((size+1)/4)-1];
					percent75 = delays[((size+1)*3/4)-1];
				}
				NumberFormat f = new DecimalFormat("#0.000");
				bw.write(web_list[i]+" "+f.format(mean)+" "+f.format(median)+" "+
						f.format(min)+" "+f.format(percent25)+" "+
						f.format(percent75)+" "+f.format(max)+"\n");
				total=0;
				index=0;
				mean=0;
				median=0;
				min=0;
				max=0;
				percent25=0;
				percent75=0;
			}
		}
		
		bw.close();
	}
	
	public static void main(String[] args) throws IOException, SQLException{
		String[] web_list_us=get_web_list("traceable_us");
		String[] web_list_eu=get_web_list("traceable_eu");
		String[] web_list_cn=get_web_list("traceable_cn");
		readProperties();
		openConnection();
		get_box_data("box_plot_data_us",web_list_us);
		get_box_data("box_plot_data_eu",web_list_eu);
		get_box_data("box_plot_data_cn",web_list_cn);
	}
}
