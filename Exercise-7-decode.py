#webView.loadData(z1.b(new String(z1.a("773032205849207A3831326F1351202E3B306B7D1E5A3B33252B382454173735266C3D3B53163735222D393B475C7A37222D7F38421B6A66643032205849206477303220584920643D2223725C503A3F39636C725F5C237A082C383C7950223F65023F3D5F4039353E3079755F5F666E1134141F5C4C64377A1B671F565A1B2C7F7B101F42700D1F39331717161574213F2B2337505D27606B712C7B0A543D342E317F214558262E636A6A6E1E4A37282233256C"), Charset.forName("UTF-8"))), "text/html", r8);
#
#// com/supercell/titan/z1.java
#public class z1 {
#    private static final char[] a = "0123456789ABCDEF".toCharArray();
#
#    public static byte[] a(String str) {
#        int length = str.length();
#        byte[] bArr = new byte[(length / 2)];
#        for (int i = 0; i < length; i += 2) {
#            bArr[i / 2] = (byte) ((Character.digit(str.charAt(i), 16) << 4) + Character.digit(str.charAt(i + 1), 16));
#        }
#        return bArr;
#    }
#
#    public static String b(String str) {
#        char[] cArr = {'K', 'C', 'Q', 'R', '1', '9', 'T', 'Z'};
#        StringBuilder sb = new StringBuilder();
#        for (int i = 0; i < str.length(); i++) {
#            sb.append((char) (str.charAt(i) ^ cArr[i % cArr.length]));
#        }
#        return sb.toString();
#    }
#}

import string

to_decode = (
    "773032205849207A3831326F1351202E3B306B7D1E5A3B33252B382454173735266C3D3B53163735222D393B475C7A37222D7F38421B6A66643032205849206477303220584920643D2223725C503A3F39636C725F5C237A082C383C7950223F65023F3D5F4039353E3079755F5F666E1134141F5C4C64377A1B671F565A1B2C7F7B101F42700D1F39331717161574213F2B2337505D27606B712C7B0A543D342E317F214558262E636A6A6E1E4A37282233256C"
)

key = string.digits + 'ABCDEF'
cArr = 'KCQR19TZ'

def a(string):
    return string.decode('hex')

def b(string):
    return ''.join(chr(ord(s_char) ^ ord(cArr[i % len(cArr)])) for i, s_char in enumerate(string))

print b(a(to_decode))
