"""Skrypt dzielący raport programu bandit na poszczególne pliki zawierające wybrane kody błędów."""

import re

codes = {
  "B101": "B101-assert_used.txt",
  "B102": "B102-exec_used.txt",
  "B103": "B103-set_bad_file_permissions.txt",
  "B104": "B104-hardcoded_bind_all_interfaces.txt",
  "B105": "B105-hardcoded_password_string.txt",
  "B106": "B106-hardcoded_password_funcarg.txt",
  "B107": "B107-hardcoded_password_default.txt",
  "B108": "B108-hardcoded_tmp_directory.txt",
  "B110": "B110-try_except_pass.txt",
  "B112": "B112-try_except_continue.txt",
  "B113": "B113-request_without_timeout.txt",
  "B201": "B201-flask_debug_true.txt",
  "B202": "B202-tarfile_unsafe_members.txt",
  "B301": "B301-pickle.txt",
  "B302": "B302-marshal.txt",
  "B303": "B303-md5.txt",
  "B304": "B304-ciphers.txt",
  "B305": "B305-cipher_modes.txt",
  "B306": "B306-mktemp_q.txt",
  "B307": "B307-eval.txt",
  "B308": "B308-mark_safe.txt",
  "B310": "B310-urllib_urlopen.txt",
  "B311": "B311-random.txt",
  "B312": "B312-telnetlib.txt",
  "B313": "B313-xml_bad_cElementTree.txt",
  "B314": "B314-xml_bad_ElementTree.txt",
  "B315": "B315-xml_bad_expatreader.txt",
  "B316": "B316-xml_bad_expatbuilder.txt",
  "B317": "B317-xml_bad_sax.txt",
  "B318": "B318-xml_bad_minidom.txt",
  "B319": "B319-xml_bad_pulldom.txt",
  "B320": "B320-xml_bad_etree.txt",
  "B321": "B321-ftplib.txt",
  "B323": "B323-unverified_context.txt",
  "B324": "B324-hashlib_insecure_functions.txt",
  "B401": "B401-import_telnetlib.txt",
  "B402": "B402-import_ftplib.txt",
  "B403": "B403-import_pickle.txt",
  "B404": "B404-import_subprocess.txt",
  "B405": "B405-import_xml_etree.txt",
  "B406": "B406-import_xml_sax.txt",
  "B407": "B407-import_xml_expat.txt",
  "B408": "B408-import_xml_minidom.txt",
  "B409": "B409-import_xml_pulldom.txt",
  "B410": "B410-import_lxml.txt",
  "B411": "B411-import_xmlrpclib.txt",
  "B412": "B412-import_httpoxy.txt",
  "B413": "B413-import_pycrypto.txt",
  "B415": "B415-import_pyghmi.txt",
  "B501": "B501-request_with_no_cert_validation.txt",
  "B502": "B502-ssl_with_bad_version.txt",
  "B503": "B503-ssl_with_bad_defaults.txt",
  "B504": "B504-ssl_with_no_version.txt",
  "B505": "B505-weak_cryptographic_key.txt",
  "B506": "B506-yaml_load.txt",
  "B507": "B507-ssh_no_host_key_verification.txt",
  "B508": "B508-snmp_insecure_version.txt",
  "B509": "B509-snmp_weak_cryptography.txt",
  "B601": "B601-paramiko_calls.txt",
  "B602": "B602-subprocess_popen_with_shell_equals_true.txt",
  "B603": "B603-subprocess_without_shell_equals_true.txt",
  "B604": "B604-any_other_function_with_shell_equals_true.txt",
  "B605": "B605-start_process_with_a_shell.txt",
  "B606": "B606-start_process_with_no_shell.txt",
  "B607": "B607-start_process_with_partial_path.txt",
  "B608": "B608-hardcoded_sql_expressions.txt",
  "B609": "B609-linux_commands_wildcard_injection.txt",
  "B610": "B610-django_extra_used.txt",
  "B611": "B611-django_rawsql_used.txt",
  "B612": "B612-logging_config_insecure_listen.txt",
  "B701": "B701-jinja2_autoescape_false.txt",
  "B702": "B702-use_of_mako_templates.txt",
  "B703": "B703-django_mark_safe.txt"
}

bandit_report = 'bandit_report.txt'


def process_report():

    """Funkcja dzieląca raport na osobne pliki względem kodu."""
    with open(bandit_report, 'r') as file:

        # Otwarcie pliku raport.txt do odczytu
        file_content = file.read()
        for i in range(100, 1000):
            code = 'B' + str(i)

            # Tworzenie wyrażenia regularnego dla danego kodu
            regex_pattern = r'^>> Issue: \[' + code + r'[\S]* [\s\S]*?-{50,}$'

            # Wyszukiwanie dopasowań przy użyciu wyrażenia regularnego
            matches = re.findall(regex_pattern, file_content, re.MULTILINE)

            # Jeśli są dopasowania, zapisz je do pliku wynikowego
            if matches:
                matched_first_block = matches[0]
                
                # Nazwa pliku wynikowego
                output_file = codes.get(code, None)
                if output_file is None:
                    output_file = code + '-' + re.search(r'\[(.*?)\:(.*?)\]', matched_first_block).group(2)

                print(f'Create: {output_file}')

                with open(output_file, 'w') as output:
                    output.write('\n'.join(matches))


if __name__ == '__main__':
    process_report()
