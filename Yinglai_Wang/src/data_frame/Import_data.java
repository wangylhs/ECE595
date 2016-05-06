package data_frame;

import java.io.*;
import java.sql.*;
import java.util.*;


public class Import_data {
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
	
	public static void createDB() throws SQLException, IOException {
		openConnection();

		Statement stat = connection.createStatement();

		// Delete the table first if any
		try {
			stat.executeUpdate("DROP TABLE ecn_data");
		}catch( Exception e) {
		}
		try {
			stat.executeUpdate("DROP TABLE beijing_data");
		}catch( Exception e) {
		}	
		// Create the table
		stat.executeUpdate("CREATE TABLE ecn_data (time VARCHAR(30), dest VARCHAR(60), " +
				"hop1 VARCHAR(30), hop2 VARCHAR(30), hop3 VARCHAR(30), " +
				"hop4 VARCHAR(30), hop5 VARCHAR(30), " +
				"hop6 VARCHAR(30), hop7 VARCHAR(30), hop8 VARCHAR(30), " +
				"hop9 VARCHAR(30), hop10 VARCHAR(30), hop11 VARCHAR(30), " +
				"hop12 VARCHAR(30), hop13 VARCHAR(30), hop14 VARCHAR(30), " +
				"hop15 VARCHAR(30), hop16 VARCHAR(30), hop17 VARCHAR(30), " +
				"hop18 VARCHAR(30), hop19 VARCHAR(30), hop20 VARCHAR(30))");
		stat.executeUpdate("CREATE TABLE beijing_data (time VARCHAR(30), dest VARCHAR(60), " +
				"hop1 VARCHAR(30), hop2 VARCHAR(30), hop3 VARCHAR(30), " +
				"hop4 VARCHAR(30), hop5 VARCHAR(30), " +
				"hop6 VARCHAR(30), hop7 VARCHAR(30), hop8 VARCHAR(30), " +
				"hop9 VARCHAR(30), hop10 VARCHAR(30), hop11 VARCHAR(30), " +
				"hop12 VARCHAR(30), hop13 VARCHAR(30), hop14 VARCHAR(30), " +
				"hop15 VARCHAR(30), hop16 VARCHAR(30), hop17 VARCHAR(30), " +
				"hop18 VARCHAR(30), hop19 VARCHAR(30), hop20 VARCHAR(30))");
	}
	
	public static void create_delay_table() throws SQLException, IOException{
		openConnection();
		Statement stat = connection.createStatement();
		try {
			stat.executeUpdate("DROP TABLE delay_data");
		}catch( Exception e) {
		}
		//create the table
		stat.executeUpdate("CREATE TABLE delay_data (time VARCHAR(30), dest VARCHAR(60), "+
				"delay DOUBLE(10,3))");
		
	}
	
	public static void insert_delay_data(String file_name) throws SQLException, IOException{
		openConnection();
		@SuppressWarnings("resource")
		BufferedReader br = new BufferedReader(new FileReader(file_name));
		String line;
		String[] s;
		String time="";
		String query;
		Statement stat = connection.createStatement();
		while((line=br.readLine())!=null){
			s = line.split(" ");
			if(s[s.length-1].equals("2016")){
				time=line;
				line=br.readLine();
				s=line.split(" ");
				
				query="INSERT INTO delay_data VALUES ('"+time+"','"+s[0]+"','"+s[2]+"')";
				System.out.println(query);
				stat.executeUpdate(query);
			}
		}
	}
	
	public static void insert_ecn_data(String file_name) throws SQLException, IOException{
		openConnection();
		@SuppressWarnings("resource")
		BufferedReader br = new BufferedReader(new FileReader(file_name));
		String line;
		int ct=0;
		String[] s;
		String query;
		String time="";
		String last_time="";
		String dest="";
		String[] trace = new String[20];
		Arrays.fill(trace,"");
		int index=0;
		Statement stat = connection.createStatement();
		while((line=br.readLine())!=null){
			s = line.split(" ");
			if(s[s.length-1].equals("2016")){
				index=0;
				time = line;
				
				query = "INSERT INTO ecn_data VALUES ('"+last_time+"','"+dest+"','" + trace[0]+
						"','"+trace[1]+"','" +trace[2]+"','" +trace[3]+"','" +trace[4] +
						"','"+trace[5]+"','" +trace[6]+"','" +trace[7]+"','" +trace[8] +
						"','"+trace[9]+"','" +trace[10]+"','" +trace[11]+"','" +trace[12] +
						"','"+trace[13]+"','" +trace[14]+"','" +trace[15]+"','" +trace[16] +
						"','"+trace[17]+"','" +trace[18]+"','" +trace[19]+"')";
				if(ct>0) {
					stat.executeUpdate(query);
				}
				
			}else if(s[0].contains("www") || s[0].contains("web")){
				index=0;
				Arrays.fill(trace, "");
				dest = s[0];
				
			}else{
				trace[index]=s[1]+" "+s[2];
				index++;
				
			}
			last_time=time;
			ct++;
		}		
	}
	
	public static void insert_beijing_data(String file_name) throws SQLException, IOException{
		openConnection();
		@SuppressWarnings("resource")
		BufferedReader br = new BufferedReader(new FileReader(file_name));
		String line;
		int ct=0;
		String[] s;
		String query;
		String time="";
		String last_time="";
		String dest="";
		String[] trace = new String[20];
		Arrays.fill(trace,"");
		int index=0;
		Statement stat = connection.createStatement();
		while((line=br.readLine())!=null){
			s = line.split(" ");
			if(s[s.length-1].equals("2016")){
				index=0;
				time = line;
				
				query = "INSERT INTO beijing_data VALUES ('"+last_time+"','"+dest+"','" + trace[0]+
						"','"+trace[1]+"','" +trace[2]+"','" +trace[3]+"','" +trace[4] +
						"','"+trace[5]+"','" +trace[6]+"','" +trace[7]+"','" +trace[8] +
						"','"+trace[9]+"','" +trace[10]+"','" +trace[11]+"','" +trace[12] +
						"','"+trace[13]+"','" +trace[14]+"','" +trace[15]+"','" +trace[16] +
						"','"+trace[17]+"','" +trace[18]+"','" +trace[19]+"')";
				//System.out.println(query);
				if(ct>0) {
					//System.out.println(time);
					stat.executeUpdate(query);
				}
				
			}else if(s[0].contains("www") || s[0].contains("web") || s[0].contains("com") 
					|| s[0].contains("edu") || s[0].contains("uk") || s[0].contains("net")
					|| s[0].contains("cn")){
				index=0;
				Arrays.fill(trace, "");
				dest = s[0];
			}else{
				//System.out.println(line);
				trace[index]=s[1]+" "+s[2];
				index++;
				
			}
			last_time=time;
			ct++;
		}		
	}
	
	public static void filte_data(String in_file, String out_file) throws IOException{
		@SuppressWarnings("resource")
		BufferedReader br = new BufferedReader(new FileReader(in_file));
		File out = new File(out_file);
		FileOutputStream fos = new FileOutputStream(out);
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));
		String line;
		String[] s;
		String time="";
		String dest="";
		String dest_ip="";
		int hop=0;
		while((line=br.readLine())!=null){
			s = line.split(" ");
			if(s[s.length-1].equals("2016")){
				//System.out.println(line);
				time = line;
				hop=1;
				//line=br.readLine();
				//s=line.split(" ");
				//dest=s[0];
			}else if(s[0].contains("www") || s[0].contains("web") || s[0].contains("com") 
					|| s[0].contains("edu") || s[0].contains("uk") || s[0].contains("net")
					|| s[0].contains("cn")){
				dest=s[0];
				dest_ip=s[1].replaceAll(",","");
				//System.out.println(time);
				//System.out.println(dest+" "+dest_ip);
				bw.write(time+"\n");
				bw.write(dest+" "+dest_ip+"\n");
			}else{
				if(s[1].equals("service") || s[0].equals("Cannot")) continue;
				if(hop>20) continue;
				if(s[1].charAt(0)>57 || s[1].contains("*") || s[2].length()>10){
					//System.out.println(s[0]+" "+s[1]+" "+s[2]);
				}else{
					//System.out.println(hop+" "+s[1]+" "+s[2]);
					bw.write(hop+" "+s[1]+" "+s[2]+"\n");
					hop++;
				}
			}
		}
		bw.close();
	}
	
	public static void get_delay_data(String in_file, String out_file)throws IOException{
		@SuppressWarnings("resource")
		BufferedReader br = new BufferedReader(new FileReader(in_file));
		File out = new File(out_file);
		FileOutputStream fos = new FileOutputStream(out);
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fos));
		String line;
		int ct=0;
		int hop=0;
		String[] s;
		String delay="";
		String dest="";
		String time="";
		String last_time="";
		while((line=br.readLine())!=null){
			s = line.split(" ");
			if(s[s.length-1].equals("2016")){
				time = line;
				if(ct>0){
					bw.write(last_time+"\n");
					bw.write(dest+" "+hop+" "+delay+"\n");
				}
				
			}else if(s[0].contains("www") || s[0].contains("web") || s[0].contains("com") 
					|| s[0].contains("edu") || s[0].contains("uk") || s[0].contains("net")
					|| s[0].contains("cn")){
				dest = s[0];
				hop=0;
				
			}else{
				System.out.println(line);
				delay=s[2];
				hop++;
			}
			last_time=time;
			ct++;
		}
		bw.close();
	}
	
	public static void main(String[] args) throws SQLException, IOException{
		readProperties();
		
		filte_data("ecn_data_eu","final_ecn_data_eu");
		filte_data("ecn_data_cn","final_ecn_data_cn");
		filte_data("ecn_data_us","final_ecn_data_us");
		filte_data("beijing_data_eu","final_beijing_data_eu");
		filte_data("beijing_data_cn","final_beijing_data_cn");
		filte_data("beijing_data_us","final_beijing_data_us");
		createDB();
		insert_ecn_data("ecn_combined_data");
		insert_beijing_data("beijing_combined_data");
		get_delay_data("ecn_combined_data","ecn_delay_data");
		get_delay_data("beijing_combined_data","beijing_delay_data");
		
		create_delay_table();
		insert_delay_data("ecn_delay_data");
	}
}
