import dns.resolver

def get_dns_server_ip():
    # تنظیم آدرس سرور DNS
    dns_server = '8.8.8.8'

    try:
        # ایجاد یک نمونه از Resolver
        resolver = dns.resolver.Resolver()

        # تنظیم آدرس سرور DNS برای Resolver
        resolver.nameservers = [dns_server]

        # درخواست رکورد A برای یک دامنه مثالی (google.com)
        answer = resolver.query('google.com', 'A')

        # استخراج آدرس IP از پاسخ
        ip_address = answer[0].address

        return ip_address
    except dns.exception.DNSException as e:
        print(f"خطا در دریافت آدرس سرور DNS: {e}")
        return None

if __name__ == "__main__":
    # دریافت آدرس سرور DNS
    dns_server_ip = get_dns_server_ip()
    if dns_server_ip:
        print(f"آدرس IP سرور DNS: {dns_server_ip}")
