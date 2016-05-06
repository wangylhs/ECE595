package data_frame;

import java.io.*;
import java.sql.*;
import java.util.*;

public class Give_path {
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
	
	public static void write_path(String web, String day, String time) 
			throws SQLException, IOException{
		Statement stat = connection.createStatement();
		ResultSet result = stat.executeQuery("SELECT * FROM ecn_data WHERE dest='"+web+"' and time like '"
				+day+"%"+time+":%'");
		String[] path = new String[700];
		Integer[] ct = new Integer[700];
		String temp="";
		String[] s;
		int current_index=0;
		Arrays.fill(ct,1);
		while(result.next()){
			for(int i=0;i<21;i++){
				s=result.getString(i+2).split(" ");
				temp += s[0]+" ";
				
			}
			for(int i=0;i<700;i++){
				if(path[i]!=null && path[i].contains(temp)){
					ct[i]++;
					temp="";
					break;
				}else if(i==699){
					//System.out.println(current_index);
					path[current_index]=temp;
					current_index++;
					temp="";
				}
			}		
		}
		int count=0;
		for(int i=0;i<700;i++){
			if(path[i]!=null){
				count++;
				s=path[i].split(" ");
				/*System.out.println(s[0]);
				for(int j=1;j<s.length;j++){
					if(j==s.length-1){
						System.out.print(s[j]+"\n");
					}else{
						System.out.print(s[j]+"->");
					}
				}*/
			}
		}
		System.out.println(web+" "+count);
		
		//System.out.println(count+" paths are taken in this time period.");
	}
	
	public static void get_target_data(String web, String day, String time) 
			throws SQLException, IOException{
		Statement stat = connection.createStatement();
		ResultSet result = stat.executeQuery("SELECT * FROM ecn_data WHERE dest='"+web+"' and time like '"
				+day+"%"+time+":%'");
		String[] path = new String[700];
		Integer[] ct = new Integer[700];
		String temp="";
		String[] s;
		int current_index=0;
		Arrays.fill(ct,1);
		while(result.next()){
			for(int i=0;i<21;i++){
				s=result.getString(i+2).split(" ");
				temp += s[0]+" ";
				
			}
			for(int i=0;i<700;i++){
				if(path[i]!=null && path[i].contains(temp)){
					ct[i]++;
					temp="";
					break;
				}else if(i==699){
					//System.out.println(current_index);
					path[current_index]=temp;
					current_index++;
					temp="";
				}
			}		
		}
		int count=0;
		for(int i=0;i<700;i++){
			if(path[i]!=null){
				count++;
				s=path[i].split(" ");
				System.out.println(s[0]);
				for(int j=1;j<s.length;j++){
					if(j==s.length-1){
						System.out.print(s[j]+"\n");
					}else{
						System.out.print(s[j]+"->");
					}
				}
			}
		}
		System.out.println(count+" paths are taken in this time period.");
	}
	
	
	
	public static void main(String[] args) throws SQLException, IOException{
		/*readProperties();
		openConnection();
		String[] web_list_us=get_web_list("traceable_us");
		String[] web_list_eu=get_web_list("traceable_eu");
		String[] web_list_cn=get_web_list("traceable_cn");
		for(int i=0;i<web_list_us.length;i++){
			if(web_list_us[i]!=null)
				write_path(web_list_us[i],"","");
		}
		for(int i=0;i<web_list_eu.length;i++){
			if(web_list_eu[i]!=null)
				write_path(web_list_eu[i],"","");
		}
		for(int i=0;i<web_list_cn.length;i++){
			if(web_list_cn[i]!=null)
				write_path(web_list_cn[i],"","");
		}*/
		@SuppressWarnings("resource")
		Scanner scanner = new Scanner( System.in );
		System.out.print( "web name(xxx.xxx.xxx): " );
		String web = scanner.nextLine();
		System.out.print( "Input a Day(Mon-Fri): " );
		String day = scanner.nextLine();
		System.out.print( "Input a time(hour): " );
		String time = scanner.nextLine();
		readProperties();
		openConnection();
		get_target_data(web,day,time);
	}
}

