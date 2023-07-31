<?php

    # XSS prevent
    header('Content-Type: text/plain');

    # DEFINE
    $code = $_POST['code'];
    $mode = $_POST['mode'];
    $data = $_POST['data'];
    $charset = $_POST['charset'];

    # CHARSET
    $charset_array = array("utf-8", "euc-kr", "ASCII", "ISO-8859-1", "utf-7", "utf-16", "utf-32");
    $charset_key = array_search($charset, $charset_array);
    $charset = $charset_array[$charset_key] ?? 'utf-8';
    #echo $charset;

    # encode
    if ($code === "0") {
        $input = iconv("utf-8",$charset,$data);

        switch ( $mode ) {

            #URL ENCODING
            case "url" :
            $result = urlencode($input);
            break;

            #BASE64 ENCODING
            case "b64" :
            $result = base64_encode($input);
            break;

            #HEX ENCODING
            case "hex" :
            $result = bin2hex($input);
            break;

        }

    }

    # decode
    elseif ( $code === "1" ) {
        
        switch ( $mode ) {
            #URL DECODING
            case "url" :
            $input = urldecode($data);
            break;

            #BASE64 DECODING
            case "b64" :
            $input = base64_decode($data);
            break;

            #HEX DECODING
            case "hex" :
            $input = pack("H*",$data);
            break;
        }

        $result = iconv($charset,"utf-8",$input);
    }

    # hash
    elseif ( $code === "2") {

        $hash_array = hash_algos();
        # ['md2','md4','md5','sha1','sha224','sha256','sha384','sha512/224','sha512/256','sha512','sha3-224','sha3-256','sha3-384','sha3-512','ripemd128','ripemd160','ripemd256','ripemd320','whirlpool','tiger128,3','tiger160,3','tiger192,3','tiger128,4','tiger160,4','tiger192,4','snefru','snefru256','gost','gost-crypto','adler32','crc32','crc32b','crc32c','fnv132','fnv1a32','fnv164','fnv1a64','joaat','murmur3a','murmur3c','murmur3f','xxh32','xxh64','xxh3','xxh128','haval128,3','haval160,3','haval192,3','haval224,3','haval256,3','haval128,4','haval160,4','haval192,4','haval224,4','haval256,4','haval128,5','haval160,5','haval192,5','haval224,5','haval256,5']
        $key = array_search($mode, $hash_array);
        
        if ($key) {
            $input = iconv("utf-8",$charset,$data);
            $result = hash($hash_array[$key],$input);
        }
    }

    # encrypt 
    elseif ( $code === "3") {
        $cipher_array = openssl_get_cipher_methods();
        $key = array_search($mode, $cipher_array);

        #if ($key) {
        #    $input = iconv("utf-8",$charset,$data);
        #    $result = hash($cipher_array[$key],$input);
        #}

        $result = "Under construction";
             
    }

    # decrypt 
    elseif ( $code === "4") {
        $cipher_array = openssl_get_cipher_methods();
        $key = array_search($mode, $cipher_array);

        #if ($key) {
        #    $input = iconv("utf-8",$charset,$data);
        #    $result = hash($cipher_array[$key],$input);
        #}

        $result = "Under construction";
  
    }


    else {
        
        $result = "Invalid code";
  
    }

    echo $result;
?>
