<?php

/**
 * Data: 2016.02
 * Author: 一把杀猪刀 blog: www.mierhuo.com
 */

interface MemcachedServerManage{
    public function addServer();
    public function delServer($serverName);
    public function checkServer($serverName);
}

interface MemcachedService{
    public function get($key);
    public function add($key,$value,$expire);
    public function delete($key);
    // 还有set,replace,...就不一一写了...
}


class MemcachedProxy implements MemcachedServerManage,MemcachedService{

    private $serverList = array(); //服务器列表，格式：hash值=>服务器编号
    private $config = null;  //存配置信息

    public function __construct(){
        $this->config = include('config.php');
        $this->addServer();
    }

    public function get($key)
    {
        return $this->getServerObj($key)->get($key);
    }

    public function add($key, $value, $expire = 0)
    {
        return $this->getServerObj($key)->add($key,$value,$expire);
    }

    public function delete($key)
    {
        return $this->getServerObj($key)->delete($key);
    }

    /**
     * 应用文中提到的一致性哈希原理取用相应服务器
     * @param $key
     * @return memcachedObj or die
     */
    protected function getServerObj($key){

        $value = $this->consistantHash($key);

        foreach($this->serverList as $k=>$serverName){
            if($k>=$value){
                if($obj = $this->checkServer($serverName)){
                    return $obj;
                }
            }
        }

        while($serverName = current($this->serverList)){
            if($obj = $this->checkServer($serverName)){
                return $obj;
            }
            $this->delServer($serverName);
            next($this->serverList);
        }

        die('无可用memcached server!');
    }

    //添加配置的服务器信息到列表(初始化操作)
    public function addServer(){
        foreach($this->config as $serverName=>$serverInfo){
            for($i=1;$i<=64;$i++){
                $tmpKey = $this->consistantHash($serverName.$i);
                $this->serverList[$tmpKey] = $serverName;
            }
        }
        ksort($this->serverList);
    }

    //从列表里删除(认为不可用的)服务器
    public function delServer($serverName){
        foreach($this->serverList as $key=>$value){
            if($value == $serverName){
                unset($this->serverList[$key]);
            }
        }
    }

    /**
     * 检测服务器是否可用
     * @param $serverName
     * @return bool|memcachedObj
     */
    public function checkServer($serverName){
        $serverInfo = $this->getServerInfo($serverName);
        $memObj = @memcache_connect($serverInfo[0], (int)$serverInfo[1]);
        if(!$memObj){
            $this->delServer($serverName);
        }
        return $memObj?$memObj:false;
    }

    //获取由服务器编号获取服务器配置信息
    protected function getServerInfo($serverName){
        if(array_key_exists($serverName,$this->config)){
            return $this->config[$serverName];
        }else{
            return false;
        }
    }

    //获取一致性hash得到的值
    protected function consistantHash($str){
        return sprintf("%u",crc32($str));
    }
}

?>