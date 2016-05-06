package data_frame;

import java.io.*;
import java.sql.*;
import java.util.*;

public class Detect_problematic {
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
		for(int i=0;i<700;i++){
			if(path[i]!=null){
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
		//System.out.println(count+" paths are taken in this time period.");
	}
	
	public static void get_problematic(String web, String day, String time)
			throws SQLException, IOException{
		Statement stat = connection.createStatement();
		ResultSet result = stat.executeQuery("SELECT * FROM ecn_data WHERE dest='"+web+"' and time like '"
				+day+"%"+time+":%'");
		String[] ip = new String[2000];
		Integer[] ct = new Integer[2000];
		Arrays.fill(ct, 0);
		int ip_index=0;
		String[] s;
		while(result.next()){
			for(int i=0;i<20;i++){
				s=result.getString(i+3).split(" ");
				//System.out.println(s[0]+" "+s[1]);
				if(s[0]!=""){
				for(int j=0;j<2000;j++){
					if(ip[j]!=null && ip[j].equals(s[0])){ 
						ct[j]++;
						break;
					}else if(j==1999){
						ip[ip_index]=s[0];
						ct[ip_index]++;
						ip_index++;
					}
				}
				}
			}
		}
		int min=50;
		for(int i=0;i<2000;i++){
			if(ip[i]!=null){
				if(ct[i]<min) min=ct[i];
			}
		}
		//System.out.println(min);
		double[] d = new double[2000];
		double max=0;
		double delay=0;
		for(int i=0;i<2000;i++){
			if(ip[i]!=null && ct[i]==min){
				//System.out.println(ip[i]+" "+ct[i]);
				for(int j=0;j<20;j++){
					result = stat.executeQuery("SELECT hop"+(j+1)+" FROM ecn_data WHERE dest='"+web+"' and " +
							"hop"+(j+1)+" like '%"+ip[i]+"%'");
					while(result.next()){
						s=result.getString(1).split(" ");
						delay = Double.valueOf(s[1]);
						d[i]=delay;
						if(max<delay) max=delay;
						if(delay>400) ct[i]=j+1;
						//System.out.println(delay);
					}
				}
			}
		}
		if(min>1 || max<400){ 
			System.out.println("There is no problematic link in this range!");
		}else{
			System.out.println("Problematic links found!");
			for(int i=0;i<2000;i++){
				if(ip[i]!=null && d[i]>400){
					System.out.println(ip[i]+" "+d[i]+" on hop"+ct[i]);
				}
			}
		}
		
	}
	
	public static void main(String[] args) throws SQLException, IOException{
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
		get_problematic(web,day,time);
	}
}

