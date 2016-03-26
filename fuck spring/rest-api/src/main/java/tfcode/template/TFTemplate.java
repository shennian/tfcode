package tfcode.template;

import java.io.UnsupportedEncodingException;

import javax.sql.DataSource;

import org.springframework.jdbc.core.JdbcTemplate;


public class TFTemplate {
	private DataSource dataSource;
	private JdbcTemplate fuckTemplate;

	public void setDataSource(DataSource dataSource) {
		this.dataSource = dataSource;
	}
	public String test() {
		fuckTemplate = new JdbcTemplate(dataSource);
		String sql = "select link_id, count from rest_search_count where kw= 'fuckyou'";
		System.out.println(sql);
		
		System.out.println(sql);
		return fuckTemplate.queryForList(sql).toString();
	}
}
